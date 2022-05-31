# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path

from cursos import views

urlpatterns = [
    # The home page
    path("", views.HomeView.as_view(), name="home"),
    path("professores/", views.ProfessorListView.as_view(), name="listar-professores"),
    path(
        "professores/cadastrar/",
        views.ProfessorCreateView.as_view(),
        name="cadastrar-professores",
    ),
    path(
        "professores/<pk>/",
        views.ProfessorUpdateView.as_view(),
        name="gerenciar-professor",
    ),
    path(
        "professores/<pk>/deletar/",
        views.ProfessorDeleteView.as_view(),
        name="deletar-professor",
    ),
    path("alunos/", views.AlunoListView.as_view(), name="listar-alunos"),
    path("alunos/cadastrar/", views.AlunoCreateView.as_view(), name="cadastrar-alunos"),
    path("alunos/<pk>/", views.AlunoUpdateView.as_view(), name="gerenciar-aluno"),
    path("alunos/<pk>/deletar/", views.AlunoDeleteView.as_view(), name="deletar-aluno"),
    path(
        "templates/alunos/",
        views.GetTemplateAlunos.as_view(),
        name="get-template-alunos",
    ),
    path(
        "planilhas/alunos/", views.PlanilhaAlunosView.as_view(), name="planilha-alunos"
    ),
    path(
        "dados-pagamento/cadastrar/",
        views.DadosPagamentoCreateView.as_view(),
        name="cadastrar-dados-pagamentos",
    ),
    path(
        "dados-pagamento/<pk>/",
        views.DadosPagamentoUpdateView.as_view(),
        name="gerenciar-dados-pagamentos",
    ),
    path("cursos/", views.CursoListView.as_view(), name="listar-cursos"),
    path("cursos/cadastrar/", views.CursoCreateView.as_view(), name="cadastrar-cursos"),
    path("cursos/<pk>/", views.CursoUpdateView.as_view(), name="gerenciar-curso"),
    path("cursos/<pk>/deletar/", views.CursoDeleteView.as_view(), name="deletar-curso"),
    path("turmas/", views.TurmaListView.as_view(), name="listar-turmas"),
    path("turmas/cadastrar/", views.TurmaCreateView.as_view(), name="cadastrar-turmas"),
    path("turmas/<pk>/", views.TurmaUpdateView.as_view(), name="gerenciar-turma"),
    path("turmas/<pk>/deletar/", views.TurmaDeleteView.as_view(), name="deletar-turma"),
    path(
        "turmas/<pk>/frequencia/",
        views.PresencaView.as_view(),
        name="visualizar-frequencia",
    ),
    path(
        "turmas/<pk>/frequencia/alunos/",
        views.PresencaAlunoView.as_view(),
        name="visualizar-frequencia-alunos",
    ),
    path(
        "turmas/<pk>/frequencia/editar/",
        views.FrequenciaUpdateView.as_view(),
        name="gerenciar-frequencia",
    ),
    path("presencas/", views.PresencaUpdateLoteView.as_view(), name="salvar-presencas"),
    path(
        "relatorios/previsao-gastos/",
        views.RelatorioPrevisaoView.as_view(),
        name="relatorio-previsao",
    ),
]
