import pylightxl as xl
import unicodedata
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Count, Sum, Q
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    DeleteView,
    FormView,
    DetailView,
)

from pessoas.forms import SendPlanilhaPessoaForm
from pessoas.models import Pessoa, Secao, Lideranca, Escola


def sanitize_str(texto):
    texto = texto.upper()
    return "".join(
        c
        for c in unicodedata.normalize("NFD", texto)
        if unicodedata.category(c) != "Mn"
    )


class PessoaListView(LoginRequiredMixin, ListView):
    model = Pessoa
    queryset = Pessoa.objects.select_related("secao__escola", "lideranca").all()
    template_name = "pessoas/pessoa_list.html"


class PessoaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Pessoa
    fields = ["nome", "lideranca", "zona", "secao"]
    success_url = reverse_lazy("cadastrar-pessoas")
    success_message = "Pessoa %(nome)s criada com sucesso."

    def form_valid(self, form):
        success_message = self.get_success_message(form.cleaned_data)
        self.object = form.save(commit=False)
        self.object.nome = sanitize_str(self.object.nome)
        self.object.save()

        if success_message:
            messages.success(self.request, success_message)

        return redirect(self.success_url)


class PessoaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Pessoa
    fields = ["nome", "lideranca", "zona", "secao"]
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
        filename = []
        erros = []
        duplicados = []
        duplicados_dict = {}
        sucesso = []
        secoes = [secao.id for secao in Secao.objects.all()]
        liderancas = {lider.nome: lider for lider in Lideranca.objects.all()}
        pessoas_dict = {
            pessoa.nome: pessoa
            for pessoa in Pessoa.objects.prefetch_related("lideranca").all()
        }
        if form.is_valid():
            filename = request.FILES["arquivo"].name
            db = xl.readxl(form.cleaned_data["arquivo"])
            for row in db.ws(ws=db.ws_names[0]).rows:
                if len(row) > 1 and row[1] and row[1] != "NOME":
                    nome = sanitize_str(row[1])
                    lider = sanitize_str(row[6])
                    pessoa_existente = pessoas_dict.get(nome)

                    if pessoa_existente:
                        if pessoa_existente.id not in duplicados_dict:
                            duplicados_dict[pessoa_existente.id] = {
                                "nome": pessoa_existente.nome,
                                "liderancas": [],
                            }
                        if (
                            pessoa_existente.lideranca.nome
                            not in duplicados_dict[pessoa_existente.id]["liderancas"]
                        ):
                            duplicados_dict[pessoa_existente.id]["liderancas"].append(
                                pessoa_existente.lideranca.nome
                            )

                        duplicados_dict[pessoa_existente.id]["liderancas"].append(lider)
                        continue

                    if lider in liderancas.keys():
                        lider = liderancas[lider]
                    else:
                        erros.append(
                            {
                                "numero": row[0],
                                "nome": nome,
                                "erro": f"Líder não encontrado: {lider}",
                            }
                        )
                        continue

                    secao = row[3] if row[3] else None
                    if secao:
                        try:
                            secao = int(secao)
                            if secao not in secoes:
                                secao = None
                        except Exception as e:
                            erros.append(
                                {
                                    "numero": row[0],
                                    "nome": nome,
                                    "erro": f"Seção deve ser um número válido. Encontrado {secao}",
                                }
                            )
                            continue

                    pessoa = Pessoa()
                    pessoa.nome = nome
                    pessoa.zona = row[2]
                    pessoa.secao_id = secao
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
                        pessoas_dict[pessoa.nome] = pessoa
                    except Exception as e:
                        erros.append(
                            {
                                "numero": row[0],
                                "nome": nome,
                                "erro": str(e).splitlines()[-1],
                            }
                        )
        for key, value in duplicados_dict.items():
            duplicados.append(
                {
                    "nome": value["nome"],
                    "liderancas": ", ".join(value["liderancas"]),
                    "status": "Apagado",
                }
            )
        if duplicados_dict:
            Pessoa.objects.filter(id__in=duplicados_dict.keys()).delete()

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


class EstatisticasView(LoginRequiredMixin, ListView):
    model = Pessoa
    queryset = Pessoa.objects.select_related("secao__escola", "lideranca").all()
    template_name = "pessoas/estatisticas.html"

    def get_context_data(self, **kwargs):
        kwargs["total"] = self.get_queryset().count()

        kwargs["pessoas_secao"] = (
            Pessoa.objects.order_by("secao_id")
            .values("secao_id")
            .annotate(qtd=Count("id"))
        )

        kwargs["pessoas_escola"] = (
            Pessoa.objects.values("secao__escola__nome")
            .annotate(qtd=Count("id"))
            .order_by("-qtd")
        )

        kwargs["pessoas_lideranca"] = (
            Pessoa.objects.values("lideranca_id", "lideranca__nome")
            .annotate(qtd=Count("id"))
            .order_by("lideranca__nome")
        )

        kwargs["pessoas_local"] = (
            Pessoa.objects.values("secao__escola__localidade")
            .annotate(qtd=Count("id"))
            .order_by("secao__escola__localidade")
        )

        return super().get_context_data(**kwargs)


class LiderancaDetailView(LoginRequiredMixin, DetailView):
    model = Lideranca
    queryset = Lideranca.objects.all()
    template_name = "pessoas/lideranca_details.html"

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        result = (
            Lideranca.objects.filter(id=self.object.id)
            .values("pessoas__secao__escola__nome")
            .annotate(qtd=Count("pessoas"))
            .values(
                "qtd",
                "pessoas__secao__escola__nome",
                "pessoas__secao__escola__localidade",
            )
        )
        total = Pessoa.objects.filter(lideranca=self.object).count()
        context = self.get_context_data(object=self.object, result=result, total=total)
        return self.render_to_response(context)


class ResultadoListView(LoginRequiredMixin, ListView):
    model = Escola
    queryset = Escola.objects.prefetch_related(
        "secoes__resultado__postulante"
    ).annotate(
        qtd_keniston=Sum(
            "secoes__resultado__quantidade",
            filter=Q(secoes__resultado__postulante__nome="KENISTON"),
            distinct=True,
        ),
        qtd_iran=Sum(
            "secoes__resultado__quantidade",
            filter=Q(secoes__resultado__postulante__nome="IRAN LIMA"),
            distinct=True,
        ),
        qtd_pessoas=Count(
            "secoes__pessoas",
            distinct=True,
        ),
    )
    template_name = "pessoas/resultado_list.html"
