from django.contrib.auth.decorators import login_required
from django.contrib.messages.views import SuccessMessageMixin
from django.http import HttpResponse
from django.template import loader
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, ListView

from cursos.models import Professor


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
    success_url = reverse_lazy("cadastrar-professores")
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
