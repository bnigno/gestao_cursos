from django.contrib.auth.decorators import login_required

from django.http import HttpResponse
from django.template import loader


@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}

    html_template = loader.get_template('cursos/index.html')
    return HttpResponse(html_template.render(context, request))
