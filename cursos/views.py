from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from cursos.models import Professor, DadosPagamentos, Aluno


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
