import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView
from workadays import workdays as wd

from cursos.forms import TurmaForm
from cursos.models import Professor, DadosPagamentos, Aluno, Curso, Turma, Frequencia


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('cursos/dashboard.html')
    return HttpResponse(html_template.render(context, request))


def list_professor(request):
    context = {'segment': 'professores'}

    html_template = loader.get_template('cursos/professor_form.html')
    return HttpResponse(html_template.render(context, request))


# def gerenciar_professores(request):
#     if request.method == "POST":
#         form = ProfessorForm(request.POST)
#         if form.is_valid():
#             post = form.save(commit=False)
#             post.author = request.user
#             post.published_date = timezone.now()
#             post.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = PostForm()
#     return render(request, 'blog/post_edit.html', {'form': form})


class ProfessorListView(ListView):
    model = Professor
    template_name = "cursos/professor_list.html"


class ProfessorCreateView(SuccessMessageMixin, CreateView):
    model = Professor
    fields = ["nome", "cpf"]
    success_url = reverse_lazy("listar-professores")
    success_message = "Professor %(nome)s criado com sucesso."


class ProfessorUpdateView(SuccessMessageMixin, UpdateView):
    model = Professor
    fields = ["nome", "cpf"]
    success_message = "Professor %(nome)s alterado com sucesso."
    template_name = "cursos/professor_form_update.html"
    success_url = reverse_lazy('listar-professores')


class ProfessorDeleteView(SuccessMessageMixin, DeleteView):
    model = Professor
    success_message = "Professor removido com sucesso."
    template_name = "cursos/professor_form_delete.html"
    success_url = reverse_lazy('listar-professores')


class DadosPagamentoCreateView(SuccessMessageMixin, CreateView):
    model = DadosPagamentos
    fields = ['tipo_pagamento', 'chave_pix', 'banco', 'agencia', 'conta', 'tipo_conta']
    template_name = "cursos/dados_pagamento_form.html"
    success_url = reverse_lazy("listar-professores")
    success_message = "Dado de pagamento criado com sucesso."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        professor_id = self.request.GET.get('professor')
        aluno_id = self.request.GET.get('aluno')

        context['professor'] = Professor.objects.get(pk=professor_id) if professor_id else None
        context['aluno'] = Aluno.objects.get(pk=aluno_id) if aluno_id else None
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


class DadosPagamentoUpdateView(SuccessMessageMixin, UpdateView):
    model = DadosPagamentos
    fields = ['tipo_pagamento', 'chave_pix', 'banco', 'agencia', 'conta', 'tipo_conta']
    template_name = "cursos/dados_pagamento_form.html"
    success_url = reverse_lazy("listar-professores")
    success_message = "Dado de pagamento atualizado com sucesso."

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        professor_id = self.request.GET.get('professor')
        aluno_id = self.request.GET.get('aluno')

        context['professor'] = Professor.objects.get(pk=professor_id) if professor_id else None
        context['aluno'] = Aluno.objects.get(pk=aluno_id) if aluno_id else None
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


class AlunoListView(ListView):
    model = Aluno
    template_name = "cursos/aluno_list.html"


class AlunoCreateView(SuccessMessageMixin, CreateView):
    model = Aluno
    fields = ["nome", "cpf"]
    success_url = reverse_lazy("listar-alunos")
    success_message = "Aluno %(nome)s criado com sucesso."


class AlunoUpdateView(SuccessMessageMixin, UpdateView):
    model = Aluno
    fields = ["nome", "cpf"]
    success_message = "Aluno %(nome)s alterado com sucesso."
    template_name = "cursos/aluno_form_update.html"
    success_url = reverse_lazy('listar-alunos')


class AlunoDeleteView(SuccessMessageMixin, DeleteView):
    model = Aluno
    success_message = "Aluno removido com sucesso."
    template_name = "cursos/aluno_form_delete.html"
    success_url = reverse_lazy('listar-alunos')


class CursoListView(ListView):
    model = Curso
    template_name = "cursos/curso_list.html"


class CursoCreateView(SuccessMessageMixin, CreateView):
    model = Curso
    fields = ["nome", "carga_horaria"]
    success_url = reverse_lazy("listar-cursos")
    success_message = "Curso %(nome)s criado com sucesso."


class CursoUpdateView(SuccessMessageMixin, UpdateView):
    model = Curso
    fields = ["nome", "carga_horaria"]
    success_message = "Curso %(nome)s alterado com sucesso."
    template_name = "cursos/curso_form_update.html"
    success_url = reverse_lazy('listar-cursos')


class CursoDeleteView(SuccessMessageMixin, DeleteView):
    model = Curso
    success_message = "Curso removido com sucesso."
    template_name = "cursos/curso_form_delete.html"
    success_url = reverse_lazy('listar-cursos')


class TurmaListView(ListView):
    model = Turma
    queryset = Turma.objects.select_related("curso", "professor", "municipio").all()
    template_name = "cursos/turma_list.html"


class TurmaCreateView(SuccessMessageMixin, CreateView):
    model = Turma
    # fields = ['curso', 'municipio', 'dt_inicio', 'dt_fim', 'professor', 'nome', 'valor_lanche', 'valor_transporte', 'alunos']
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
                frequencia.has_aula = wd.is_workday(start_date, country='BR', state="PA")
                frequencia.save()
                start_date += delta

        if success_message:
            messages.success(self.request, success_message)
        return redirect(reverse("listar-turmas"))


class TurmaUpdateView(SuccessMessageMixin, UpdateView):
    model = Turma
    # fields = ['curso', 'municipio', 'dt_inicio', 'dt_fim', 'professor', 'nome', 'valor_lanche', 'valor_transporte', 'alunos']
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
                if not Frequencia.objects.filter(turma=self.object, data=start_date).exists():
                    frequencia = Frequencia()
                    frequencia.turma = self.object
                    frequencia.data = start_date
                    frequencia.has_aula = wd.is_workday(start_date, country='BR', state="PA")
                    frequencia.save()
                start_date += delta

        if success_message:
            messages.success(self.request, success_message)
        return redirect(reverse("listar-turmas"))


class TurmaDeleteView(SuccessMessageMixin, DeleteView):
    model = Turma
    success_message = "Turma removida com sucesso."
    template_name = "cursos/turma_form_delete.html"
    success_url = reverse_lazy('listar-turmas')
