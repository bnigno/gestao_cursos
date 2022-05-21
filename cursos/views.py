import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.db.models import Prefetch, F, Count, Q
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
    ListView,
    DetailView,
)
from django.views.generic.edit import FormView
from workadays import workdays as wd

from cursos.forms import TurmaForm, FrequenciaForm, PresencaForm, DatasFrequenciaForm
from cursos.models import (
    Professor,
    DadosPagamentos,
    Aluno,
    Curso,
    Turma,
    Frequencia,
    FrequenciaAluno,
)


class HomeView(LoginRequiredMixin, ListView):
    model = Turma
    queryset = Turma.objects.select_related("curso").all()
    template_name = "cursos/dashboard.html"

    def get_context_data(self, **kwargs):
        series_lanche = []
        series_transporte = []
        labels = []
        hoje = datetime.date.today()
        custo_por_mes = (
            Turma.objects.filter(
                dt_inicio__lte=hoje,
                frequencia__has_aula=True,
                frequencia__data__lte=hoje,
            )
            .values("frequencia__data__year", "frequencia__data__month")
            .annotate(
                dias_uteis=Count("frequencia"),
                presencas=Count(
                    "frequencia__alunos__presente",
                    filter=Q(frequencia__alunos__presente=True),
                ),
            )
            .annotate(
                custo_lanche=F("valor_lanche") * F("dias_uteis"),
                custo_transporte=F("valor_transporte") * F("presencas"),
            )
            .order_by("frequencia__data__year", "frequencia__data__month")
        )

        for data in custo_por_mes:
            labels.append(
                datetime.date(
                    data["frequencia__data__year"], data["frequencia__data__month"], 1
                ).strftime("%b/%y")
            )
            series_lanche.append(data["custo_lanche"])
            series_transporte.append(data["custo_transporte"])

        kwargs["series"] = [series_lanche, series_transporte]
        kwargs["labels"] = labels

        kwargs["turmas"] = (
            Turma.objects.select_related("curso", "professor", "municipio")
            .filter(dt_inicio__lte=hoje, dt_fim__gte=hoje)
            .all()
        )

        kwargs["total_alunos"] = Aluno.objects.count()
        kwargs["total_turmas"] = Turma.objects.count()

        return super().get_context_data(**kwargs)


def gerenciar_professores(request):
    return render(request, "cursos/index.html")


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
    template_name = "cursos/aluno_list.html"


class AlunoCreateView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
    model = Aluno
    fields = ["nome", "cpf"]
    success_url = reverse_lazy("listar-alunos")
    success_message = "Aluno %(nome)s criado com sucesso."


class AlunoUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Aluno
    fields = ["nome", "cpf"]
    success_message = "Aluno %(nome)s alterado com sucesso."
    template_name = "cursos/aluno_form_update.html"
    success_url = reverse_lazy("listar-alunos")


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
    queryset = Turma.objects.select_related("curso", "professor", "municipio").all()
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


# class TurmaViewSet(viewsets.ModelViewSet):
#     queryset = Turma.objects.all()
#     serializer_class = TurmaAlunoSerializer
#     permission_classes = [permissions.IsAuthenticated]
#     filter_backends = (DjangoFilterBackend,)
#
#     def retrieve(self, request, *args, **kwargs):
#         result = []
#         obj = self.get_object()
#         dict_houve_aula = {"nome": "Houve aula?"}
#         for frequencia in Frequencia.objects.filter(turma=obj).order_by("data").all():
#             dict_houve_aula[frequencia.data.strftime('%Y-%m-%d')] = frequencia.has_aula
#         result.append(dict_houve_aula)
#         for aluno in obj.alunos.order_by("nome").all():
#             aluno_dict = {"nome": aluno.nome}
#             for frequencia in Frequencia.objects.filter(turma=obj).order_by("data").all():
#                 frequencia_aluno = FrequenciaAluno.objects.filter(frequencia=frequencia, aluno=aluno).first()
#                 aluno_dict[frequencia.data.strftime('%Y-%m-%d')] = frequencia_aluno.presente if frequencia_aluno else False
#             result.append(aluno_dict)
#         return Response(
#             result, status=status.HTTP_200_OK
#         )


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

        for aluno in obj.alunos.all():
            frequencia_total = FrequenciaAluno.objects.filter(
                frequencia__turma=obj,
                aluno=aluno,
                frequencia__data__in=datas,
                presente=True,
            ).count()

            linha = [
                aluno.nome,
                frequencia_total,
                obj.valor_transporte,
                frequencia_total * obj.valor_transporte,
                aluno.dados_pagamento,
            ]
            linhas.append(linha)

        kwargs["headers"] = headers
        kwargs["linhas"] = linhas
        return super().get_context_data(**kwargs)
