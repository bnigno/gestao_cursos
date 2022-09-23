import pylightxl as xl
import unicodedata
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from pessoas.forms import SendPlanilhaPessoaForm
from pessoas.models import Pessoa


def sanitize_str(texto):
    texto = texto.upper()
    return "".join(
        c
        for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


class PessoaListView(LoginRequiredMixin, ListView):
    model = Pessoa
    queryset = Pessoa.objects.all()
    template_name = "pessoas/pessoa_list.html"


class PessoaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Pessoa
    fields = ["nome", "lideranca", "zona", "secao", "escola", "localidade"]
    success_url = reverse_lazy("cadastrar-pessoas")
    success_message = "Pessoa %(nome)s criada com sucesso."

    def form_valid(self, form):
        success_message = self.get_success_message(form.cleaned_data)
        self.object = form.save(commit=False)
        self.object.nome = sanitize_str(self.object.nome)
        if self.object.escola:
            self.object.escola = sanitize_str(self.object.escola)
        if self.object.localidade:
            self.object.localidade = sanitize_str(self.object.localidade)
        self.object.save()

        if success_message:
            messages.success(self.request, success_message)

        return redirect(self.success_url)


class PessoaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Pessoa
    fields = ["nome", "lideranca", "zona", "secao", "escola", "localidade"]
    success_message = "Pessoa %(nome)s alterada com sucesso."
    template_name = "pessoas/pessoa_form_update.html"
    success_url = reverse_lazy("listar-pessoas")

    def form_valid(self, form):
        success_message = self.get_success_message(form.cleaned_data)
        self.object = form.save(commit=False)
        self.object.nome = sanitize_str(self.object.nome)
        if self.object.escola:
            self.object.escola = sanitize_str(self.object.escola)
        if self.object.localidade:
            self.object.localidade = sanitize_str(self.object.localidade)
        self.object.save()

        if success_message:
            messages.success(self.request, success_message)

        return redirect(self.success_url)


class PessoaDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Pessoa
    success_message = "Pessoa removida com sucesso."
    template_name = "pessoas/pessoa_form_delete.html"
    success_url = reverse_lazy("listar-pessoas")


class GetTemplatePessoas(View):
    def get(self, request):
        path = "static/template/template_cadastro_pessoas.xlsx"

        file = open(path, "rb")

        response = HttpResponse(
            file.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response[
            "Content-Disposition"
        ] = "attachment; filename=template_cadastro_pessoas.xlsx"
        return response


class PlanilhaPessoasView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "pessoas/planilha_form.html"
    form_class = SendPlanilhaPessoaForm
    success_url = reverse_lazy("listar-pessoas")
    success_message = "Planilha importada com sucesso"

    def post(self, request, *args, **kwargs):
        form = SendPlanilhaPessoaForm(request.POST, request.FILES)
        erros = []
        duplicados = []
        sucesso = []
        if form.is_valid():
            filename = request.FILES["arquivo"].name
            db = xl.readxl(form.cleaned_data["arquivo"])
            lider = form.cleaned_data["lideranca"]
            for row in db.ws(ws=db.ws_names[0]).rows:
                if row[1] and row[1] != "NOME":
                    nome = sanitize_str(row[1])
                    pessoa_existente = (
                        Pessoa.objects.prefetch_related("lideranca")
                        .filter(nome=nome)
                        .first()
                    )
                    if pessoa_existente:
                        duplicados.append(
                            {
                                "nome": row[1],
                                "lideranca": pessoa_existente.lideranca.nome,
                                "status": "Apagado",
                            }
                        )
                        pessoa_existente.delete()
                        continue
                    pessoa = Pessoa()
                    pessoa.nome = nome
                    pessoa.zona = row[2]
                    pessoa.secao = row[3] if row[3] else None
                    pessoa.escola = sanitize_str(row[4])
                    pessoa.localidade = sanitize_str(row[5])
                    pessoa.lideranca = lider
                    try:
                        pessoa.save()
                        sucesso.append(
                            {
                                "nome": pessoa.nome,
                                "lideranca": lider.nome,
                                "status": "Criado",
                            }
                        )
                    except Exception as e:
                        erros.append(
                            {
                                "numero": row[0],
                                "nome": nome,
                                "erro": str(e).splitlines()[-1],
                            }
                        )

        if not erros:
            messages.success(self.request, self.success_message)
        else:
            messages.error(
                self.request,
                f"Houveram {len(erros)} erros durante o processamento da planilha.",
            )
        return render(
            self.request,
            "pessoas/status_planilha.html",
            context={
                "sucessos": sucesso,
                "erros": erros,
                "duplicados": duplicados,
                "filename": filename,
            },
        )
