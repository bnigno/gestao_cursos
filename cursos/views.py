import datetime
import re

import pylightxl as xl
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Prefetch, F, Count, Q, Value
from django.db.models.functions import Concat
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.views import View
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
)
from django.views.generic.edit import FormView
from workadays import workdays as wd

from cursos.forms import (
    TurmaForm,
    FrequenciaForm,
    PresencaForm,
    DatasFrequenciaForm,
    DadosPagamentosForm,
    SendPlanilhaForm,
)
from cursos.models import (
    Professor,
    DadosPagamentos,
    Aluno,
    Curso,
    Turma,
    Frequencia,
    FrequenciaAluno,
    Municipio,
)


class HomeView(LoginRequiredMixin, ListView):
    model = Turma
    queryset = Turma.objects.select_related("curso").all()
    template_name = "cursos/dashboard.html"

    def get_context_data(self, **kwargs):
        # series_lanche = []
        # series_transporte = []
        # labels = []
        hoje = datetime.date.today()
        # datas = (
        #     Turma.objects.filter(
        #         dt_inicio__lte=hoje,
        #         frequencia__data__lte=hoje,
        #     )
        #     .annotate(
        #         data_format=Concat(
        #             F("frequencia__data__year"),
        #             Value("-"),
        #             F("frequencia__data__month"),
        #             Value("-"),
        #             Value(1),
        #             output_field=DateField(),
        #         )
        #     )
        #     .distinct("data_format")
        #     .order_by("data_format")
        #     .values("data_format")
        # )
        #
        # for data in datas:
        #     ano = data["data_format"].split("-")[0]
        #     mes = data["data_format"].split("-")[1]
        #     labels.append(datetime.date(ano, mes, 1))
        #     dias_uteis = Frequencia.objects.filter(
        #         has_aula=True,
        #         data__month=mes,
        #         data__year=ano,
        #     ).count()
        #     presencas = FrequenciaAluno.objects.filter(
        #         frequencia__data__month=mes,
        #         frequencia__data__year=ano,
        #         frequencia__has_aula=True,
        #         presente=True,
        #     ).count()
        #     # series_lanche.append(dias_uteis)
        #     series_transporte.append(data["custo_transporte"])
        #
        # kwargs["series"] = [series_lanche, series_transporte]
        # kwargs["labels"] = labels
        #
        # # kwargs["series"] = [series_lanche]
        # # kwargs["labels"] = labels
        #
        kwargs["turmas"] = (
            Turma.objects.select_related("curso", "professor", "municipio")
            .filter(dt_inicio__lte=hoje, dt_fim__gte=hoje)
            .all()
        )

        kwargs["total_alunos"] = Aluno.objects.count()
        kwargs["total_turmas"] = Turma.objects.count()

        return super().get_context_data(**kwargs)


class ProfessorListView(LoginRequiredMixin, ListView):
    model = Professor
    template_name = "cursos/professor_list.html"
    login_required()


class ProfessorCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Professor
    fields = ["nome", "cpf"]
    success_url = reverse_lazy("listar-professores")
    success_message = "Professor %(nome)s criado com sucesso."


class ProfessorUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Professor
    fields = ["nome", "cpf"]
    success_message = "Professor %(nome)s alterado com sucesso."
    template_name = "cursos/professor_form_update.html"
    success_url = reverse_lazy("listar-professores")


class ProfessorDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Professor
    success_message = "Professor removido com sucesso."
    template_name = "cursos/professor_form_delete.html"
    success_url = reverse_lazy("listar-professores")


class DadosPagamentoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = DadosPagamentos
    fields = ["tipo_pagamento", "chave_pix", "banco", "agencia", "conta", "tipo_conta"]
    template_name = "cursos/dados_pagamento_form.html"
    success_url = reverse_lazy("listar-professores")
    success_message = "Dado de pagamento criado com sucesso."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        professor_id = self.request.GET.get("professor")
        aluno_id = self.request.GET.get("aluno")

        context["professor"] = (
            Professor.objects.get(pk=professor_id) if professor_id else None
        )
        context["aluno"] = Aluno.objects.get(pk=aluno_id) if aluno_id else None
        return context

    def form_valid(self, form):
        success_message = self.get_success_message(form.cleaned_data)
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.save()

            if success_message:
                messages.success(self.request, success_message)

            professor_id = self.request.POST.get("professor_id")
            aluno_id = self.request.POST.get("aluno_id")

            if professor_id:
                professor = Professor.objects.get(pk=professor_id)
                professor.dados_pagamento = self.object
                professor.save()
                return redirect(reverse("listar-professores"))
            if aluno_id:
                aluno = Aluno.objects.get(pk=aluno_id)
                aluno.dados_pagamento = self.object
                aluno.save()
                return redirect(reverse("listar-alunos"))

        return redirect(reverse("listar-professores"))


class DadosPagamentoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = DadosPagamentos
    fields = ["tipo_pagamento", "chave_pix", "banco", "agencia", "conta", "tipo_conta"]
    template_name = "cursos/dados_pagamento_form.html"
    success_url = reverse_lazy("listar-professores")
    success_message = "Dado de pagamento atualizado com sucesso."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        professor_id = self.request.GET.get("professor")
        aluno_id = self.request.GET.get("aluno")

        context["professor"] = (
            Professor.objects.get(pk=professor_id) if professor_id else None
        )
        context["aluno"] = Aluno.objects.get(pk=aluno_id) if aluno_id else None
        return context

    def form_valid(self, form):
        success_message = self.get_success_message(form.cleaned_data)
        with transaction.atomic():
            self.object = form.save(commit=False)
            self.object.save()

            if success_message:
                messages.success(self.request, success_message)

            professor_id = self.request.POST.get("professor_id")
            aluno_id = self.request.POST.get("aluno_id")

            if professor_id:
                professor = Professor.objects.get(pk=professor_id)
                professor.dados_pagamento = self.object
                professor.save()
                return redirect(reverse("listar-professores"))
            if aluno_id:
                aluno = Aluno.objects.get(pk=aluno_id)
                aluno.dados_pagamento = self.object
                aluno.save()
                return redirect(reverse("listar-alunos"))

        return redirect(reverse("listar-professores"))


class AlunoListView(LoginRequiredMixin, ListView):
    model = Aluno
    queryset = (
        Aluno.objects.select_related(
            "dados_pagamento", "dados_pagamento__tipo_pagamento"
        )
        .prefetch_related("turmas__curso")
        .all()
    )
    template_name = "cursos/aluno_list.html"


class AlunoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Aluno
    fields = ["nome", "cpf"]
    success_url = reverse_lazy("cadastrar-alunos")
    success_message = "Aluno %(nome)s criado com sucesso."

    def get_context_data(self, **kwargs):
        kwargs["dados_pagamento_form"] = DadosPagamentosForm()
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        success_message = self.get_success_message(form.cleaned_data)
        with transaction.atomic():
            self.object = form.save(commit=False)
            dados_pagamentos = DadosPagamentosForm(self.request.POST).save()
            self.object.dados_pagamento = dados_pagamentos
            self.object.save()

            if success_message:
                messages.success(self.request, success_message)

        return redirect(self.success_url)


class AlunoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Aluno
    fields = ["nome", "cpf"]
    success_message = "Aluno %(nome)s alterado com sucesso."
    template_name = "cursos/aluno_form_update.html"
    success_url = reverse_lazy("listar-alunos")

    def get_context_data(self, **kwargs):

        if not self.object.dados_pagamento:
            kwargs["dados_pagamento_form"] = DadosPagamentosForm(
                instance=self.object.dados_pagamento, initial=[("aluno", self.object)]
            )
        else:
            kwargs["dados_pagamento_form"] = DadosPagamentosForm(
                instance=self.object.dados_pagamento
            )

        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        success_message = self.get_success_message(form.cleaned_data)
        with transaction.atomic():
            self.object = form.save()

            if self.object.dados_pagamento:
                DadosPagamentosForm(
                    self.request.POST, instance=self.object.dados_pagamento
                ).save()
            else:
                dados_pagamentos = DadosPagamentosForm(self.request.POST).save()
                self.object.dados_pagamento = dados_pagamentos
                self.object.save()

            if success_message:
                messages.success(self.request, success_message)

        return redirect(self.success_url)


class AlunoDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Aluno
    success_message = "Aluno removido com sucesso."
    template_name = "cursos/aluno_form_delete.html"
    success_url = reverse_lazy("listar-alunos")


class CursoListView(LoginRequiredMixin, ListView):
    model = Curso
    template_name = "cursos/curso_list.html"


class CursoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Curso
    fields = ["nome", "carga_horaria"]
    success_url = reverse_lazy("listar-cursos")
    success_message = "Curso %(nome)s criado com sucesso."


class CursoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Curso
    fields = ["nome", "carga_horaria"]
    success_message = "Curso %(nome)s alterado com sucesso."
    template_name = "cursos/curso_form_update.html"
    success_url = reverse_lazy("listar-cursos")


class CursoDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Curso
    success_message = "Curso removido com sucesso."
    template_name = "cursos/curso_form_delete.html"
    success_url = reverse_lazy("listar-cursos")


class TurmaListView(LoginRequiredMixin, ListView):
    model = Turma
    queryset = (
        Turma.objects.select_related("curso", "professor", "municipio")
        .prefetch_related(Prefetch("alunos", queryset=Aluno.objects.order_by("nome")))
        .all()
    )
    template_name = "cursos/turma_list.html"


class TurmaCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Turma
    template_name = "cursos/turma_form.html"
    form_class = TurmaForm
    success_url = reverse_lazy("listar-turmas")
    success_message = "Turma criada com sucesso."

    def form_valid(self, form):
        success_message = self.get_success_message(form.cleaned_data)
        with transaction.atomic():
            self.object = form.save()

            start_date = self.object.dt_inicio
            end_date = self.object.dt_fim
            delta = datetime.timedelta(days=1)

            while start_date <= end_date:
                frequencia = Frequencia()
                frequencia.turma = self.object
                frequencia.data = start_date
                frequencia.has_aula = wd.is_workday(
                    start_date, country="BR", state="PA"
                )
                frequencia.save()
                for aluno in self.object.alunos.all():
                    FrequenciaAluno.objects.create(frequencia=frequencia, aluno=aluno)
                start_date += delta

        if success_message:
            messages.success(self.request, success_message)
        return redirect(reverse("listar-turmas"))


class TurmaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Turma
    template_name = "cursos/turma_form_update.html"
    form_class = TurmaForm
    success_url = reverse_lazy("listar-turmas")
    success_message = "Turma criada com sucesso."

    def form_valid(self, form):
        success_message = self.get_success_message(form.cleaned_data)
        with transaction.atomic():
            self.object = form.save()

            start_date = self.object.dt_inicio
            end_date = self.object.dt_fim
            delta = datetime.timedelta(days=1)

            Frequencia.objects.filter(turma=self.object, data__lt=start_date).delete()
            Frequencia.objects.filter(turma=self.object, data__gt=end_date).delete()

            while start_date <= end_date:
                if not Frequencia.objects.filter(
                    turma=self.object, data=start_date
                ).exists():
                    frequencia = Frequencia()
                    frequencia.turma = self.object
                    frequencia.data = start_date
                    frequencia.has_aula = wd.is_workday(
                        start_date, country="BR", state="PA"
                    )
                    frequencia.save()
                start_date += delta

            for frequencia in self.object.frequencia_set.all():
                if frequencia.has_aula:
                    for aluno in self.object.alunos.all():
                        presenca = FrequenciaAluno.objects.filter(
                            frequencia=frequencia, aluno=aluno
                        ).first()
                        if not presenca:
                            FrequenciaAluno.objects.create(
                                frequencia=frequencia, aluno=aluno
                            )
                else:
                    for aluno in self.object.alunos.all():
                        presenca = FrequenciaAluno.objects.filter(
                            frequencia=frequencia, aluno=aluno
                        ).first()
                        if not presenca:
                            FrequenciaAluno.objects.create(
                                frequencia=frequencia, aluno=aluno
                            )
                        elif presenca.presente:
                            presenca.presente = False
                            presenca.save()

            FrequenciaAluno.objects.filter(frequencia__turma=self.object).exclude(
                aluno__in=self.object.alunos.all()
            ).delete()

        if success_message:
            messages.success(self.request, success_message)
        return redirect(reverse("listar-turmas"))


class TurmaDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Turma
    success_message = "Turma removida com sucesso."
    template_name = "cursos/turma_form_delete.html"
    success_url = reverse_lazy("listar-turmas")


class FrequenciaUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Turma
    fields = []
    template_name = "cursos/frequencia_form.html"
    success_url = reverse_lazy("gerenciar-frequencia")
    success_message = "Frequência salva com sucesso."
    queryset = (
        Turma.objects.select_related("curso")
        .prefetch_related("frequencia_set__alunos")
        .all()
    )

    def get_context_data(self, **kwargs):
        data_selecionada = self.request.GET.get("data_list")

        try:
            data_selecionada = datetime.datetime.strptime(
                data_selecionada, "%Y-%m-%d"
            ).date()
        except:
            data_selecionada = None

        form_datas = DatasFrequenciaForm(
            [
                (data, data)
                for data in self.object.frequencia_set.order_by("data").values_list(
                    "data", flat=True
                )
            ]
        )

        if data_selecionada:
            kwargs["data_selecionada"] = data_selecionada
            form_datas.fields["data_list"].initial = [data_selecionada]
            frequencia = Frequencia.objects.get(
                turma=self.object, data=data_selecionada
            )
            kwargs["form_presenca"] = FrequenciaForm(instance=frequencia)

            PresencaFormset = modelformset_factory(
                FrequenciaAluno, form=PresencaForm, extra=0
            )
            formset = PresencaFormset(
                queryset=FrequenciaAluno.objects.filter(frequencia=frequencia)
                .order_by("aluno__nome")
                .all()
            )
            kwargs["alunos_formset"] = formset
            kwargs["frequencia_id"] = frequencia.id

        kwargs["datas"] = form_datas
        return super().get_context_data(**kwargs)

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        post_data = self.request.POST
        frequencia = Frequencia.objects.get(
            turma=post_data["turma"], data=post_data["data"]
        )
        frequencia.has_aula = True if "has_aula" in post_data.keys() else False
        frequencia.save()

        url = reverse_lazy("gerenciar-frequencia", kwargs={"pk": post_data["turma"]})
        success_url = f"{url}?data_list={post_data['data']}"
        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(success_url)


class PresencaUpdateLoteView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    def post(self, request, *args, **kwargs):
        PresencaFormset = modelformset_factory(
            FrequenciaAluno, form=PresencaForm, extra=0
        )
        formset = PresencaFormset(request.POST)
        instances = formset.save()
        frequencia = Frequencia.objects.get(pk=request.POST.get("frequencia_id"))

        url = reverse_lazy("gerenciar-frequencia", kwargs={"pk": frequencia.turma_id})
        messages.success(
            request,
            f"Presenças do dia {frequencia.data.strftime('%d/%m/%Y')} salvas com sucesso",
        )
        success_url = f"{url}?data_list={frequencia.data.strftime('%Y-%m-%d')}"
        return HttpResponseRedirect(success_url)


class PresencaView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Turma
    queryset = (
        Turma.objects.select_related("curso")
        .prefetch_related(
            Prefetch("alunos", queryset=Aluno.objects.order_by("nome")),
            Prefetch(
                "frequencia_set",
                queryset=Frequencia.objects.filter(has_aula=True).order_by("data"),
            ),
        )
        .all()
    )
    template_name = "cursos/turma_frequencia.html"

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        linhas = []
        headers = ["Nome"]
        datas = []
        total_geral = 0
        frequencias = obj.frequencia_set.all()
        dt_inicio = self.request.GET.get("dt_inicio")
        dt_fim = self.request.GET.get("dt_fim")

        if dt_inicio:
            frequencias = frequencias.filter(data__gte=dt_inicio)
        if dt_fim:
            frequencias = frequencias.filter(data__lte=dt_fim)

        for f in frequencias:
            datas.append(f.data)
        headers += datas + ["Frequência", "Valor Diário", "Valor Total"]

        for aluno in obj.alunos.all():
            linha = [aluno.nome]
            frequencia_total = 0
            for presenca in FrequenciaAluno.objects.filter(
                frequencia__turma=obj, aluno=aluno, frequencia__data__in=datas
            ).order_by("frequencia__data"):
                frequencia_total += 1 if presenca.presente else 0
                linha.append(presenca.presente)
            linha += [
                frequencia_total,
                obj.valor_transporte,
                frequencia_total * obj.valor_transporte,
            ]
            linhas.append(linha)
            total_geral += frequencia_total * obj.valor_transporte

        kwargs["headers"] = headers
        kwargs["linhas"] = linhas
        kwargs["total_geral"] = total_geral
        return super().get_context_data(**kwargs)


class PresencaAlunoView(LoginRequiredMixin, SuccessMessageMixin, DetailView):
    model = Turma
    queryset = (
        Turma.objects.select_related("curso")
        .prefetch_related(
            Prefetch(
                "alunos",
                queryset=Aluno.objects.select_related("dados_pagamento").order_by(
                    "nome"
                ),
            ),
            Prefetch(
                "frequencia_set",
                queryset=Frequencia.objects.filter(has_aula=True).order_by("data"),
            ),
        )
        .all()
    )
    template_name = "cursos/turma_frequencia_aluno.html"

    def get_context_data(self, **kwargs):
        obj = self.get_object()
        linhas = []
        datas = []
        frequencias = obj.frequencia_set.all()
        dt_inicio = self.request.GET.get("dt_inicio")
        dt_fim = self.request.GET.get("dt_fim")

        if dt_inicio:
            frequencias = frequencias.filter(data__gte=dt_inicio)
        if dt_fim:
            frequencias = frequencias.filter(data__lte=dt_fim)

        for f in frequencias:
            datas.append(f.data)
        headers = [
            "Nome",
            "Frequência",
            "Valor Diário",
            "Valor Total",
            "Dados de Pagamento",
        ]

        total_geral = 0

        for aluno in obj.alunos.all():
            frequencia_total = FrequenciaAluno.objects.filter(
                frequencia__turma=obj,
                aluno=aluno,
                frequencia__data__in=datas,
                presente=True,
            ).count()

            valor_aluno = frequencia_total * obj.valor_transporte

            linha = [
                aluno.nome,
                frequencia_total,
                obj.valor_transporte,
                valor_aluno,
                aluno.dados_pagamento,
            ]
            linhas.append(linha)
            total_geral += valor_aluno

        kwargs["headers"] = headers
        kwargs["linhas"] = linhas
        kwargs["total_geral"] = total_geral
        return super().get_context_data(**kwargs)


class GetTemplateAlunos(View):
    def get(self, request):
        path = "static/template/template_cadastro_alunos.xlsx"

        file = open(path, "rb")

        response = HttpResponse(
            file.read(),
            content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        response[
            "Content-Disposition"
        ] = "attachment; filename=template_cadastro_alunos.xlsx"
        return response


class PlanilhaAlunosView(LoginRequiredMixin, SuccessMessageMixin, FormView):
    template_name = "cursos/planilha_form.html"
    form_class = SendPlanilhaForm
    success_url = reverse_lazy("listar-alunos")
    success_message = "Planilha importada com sucesso"

    def post(self, request, *args, **kwargs):
        form = SendPlanilhaForm(request.POST, request.FILES)
        if form.is_valid():
            db = xl.readxl(form.cleaned_data["arquivo"])
            for row in db.ws(ws=db.ws_names[0]).rows:
                with transaction.atomic():
                    if row[0] and row[0] != "Nome":
                        aluno = Aluno()
                        aluno.nome = row[0]
                        aluno.cpf = row[1] if row[1] else None
                        dados_pagamento = None
                        if row[2]:
                            dados_pagamento = DadosPagamentos()
                            dados_pagamento.tipo_pagamento_id = 1
                            dados_pagamento.chave_pix = row[2]
                        elif row[3] and row[4] and row[5] and row[6]:
                            dados_pagamento = DadosPagamentos()
                            dados_pagamento.tipo_pagamento_id = 2
                            dados_pagamento.banco = row[3]
                            dados_pagamento.agencia = row[4]
                            dados_pagamento.conta = row[5]
                            dados_pagamento.tipo_conta = (
                                1 if re.search(r"corrente", row[6], re.I) else 2
                            )

                        if dados_pagamento:
                            dados_pagamento.save()
                            aluno.dados_pagamento = dados_pagamento
                        aluno.save()

        messages.success(self.request, self.success_message)
        return HttpResponseRedirect(self.success_url)


class RelatorioPrevisaoView(LoginRequiredMixin, ListView):
    model = Frequencia
    # queryset = Turma.objects.select_related("curso").prefetch_related("frequencia_set__alunos").all()
    queryset = Frequencia.objects.select_related("turma__curso").all()
    template_name = "cursos/relatorio-previsao-gastos.html"

    def get_context_data(self, **kwargs):
        dt_inicio = self.request.GET.get("dt_inicio")
        dt_fim = self.request.GET.get("dt_fim")
        total = 0
        linhas = []
        if dt_inicio and dt_fim:
            for turma in (
                self.get_queryset()
                .filter(data__gte=dt_inicio, data__lte=dt_fim)
                .values("turma")
                .annotate(
                    dias_uteis=Count("id", filter=Q(has_aula=True), distinct=True),
                    qtd_alunos=Count("turma__alunos", distinct=True),
                    nome_turma=Concat(
                        "turma__curso__nome", Value(" - "), "turma__municipio__nome"
                    ),
                )
                .annotate(
                    total_lanche=F("turma__valor_lanche") * F("dias_uteis"),
                    total_transporte=F("turma__valor_transporte")
                    * F("qtd_alunos")
                    * F("dias_uteis"),
                )
            ):
                total_linha = turma["total_lanche"] + turma["total_transporte"]
                linhas.append(
                    [
                        turma["nome_turma"],
                        turma["total_lanche"],
                        turma["total_transporte"],
                        total_linha,
                    ]
                )
                total += total_linha

            kwargs["linhas"] = linhas
            kwargs["total"] = total

            return super().get_context_data(**kwargs)


class RelatorioLancheView(LoginRequiredMixin, ListView):
    model = Turma
    queryset = Turma.objects.select_related("curso", "municipio").all()

    template_name = "cursos/relatorio-lanche.html"

    def get_context_data(self, **kwargs):
        dt_inicio = self.request.GET.get("dt_inicio")
        dt_fim = self.request.GET.get("dt_fim")
        municipio = self.request.GET.get("municipio")
        total = 0
        linhas = []
        kwargs["municipios"] = Municipio.objects.filter(
            id__in=Turma.objects.values_list("municipio_id", flat=True)
        ).all()

        if municipio:
            self.queryset = self.get_queryset().filter(municipio_id=municipio)

        if dt_inicio and dt_fim:
            for turma in (
                self.get_queryset()
                .annotate(
                    dias_uteis=Count(
                        "frequencia__id",
                        filter=Q(
                            frequencia__has_aula=True,
                            frequencia__data__gte=dt_inicio,
                            frequencia__data__lte=dt_fim,
                        ),
                        distinct=True,
                    ),
                    nome_turma=Concat("curso__nome", Value(" - "), "municipio__nome"),
                )
                .annotate(total_lanche=F("valor_lanche") * F("dias_uteis"))
            ).values():
                linhas.append(
                    [
                        turma["nome_turma"],
                        turma["dias_uteis"],
                        turma["valor_lanche"],
                        turma["valor_lanche"] * turma["dias_uteis"],
                    ]
                )
                total += turma["total_lanche"]

            kwargs["linhas"] = linhas
            kwargs["total"] = total

        return super().get_context_data(**kwargs)
