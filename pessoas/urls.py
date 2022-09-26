# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path

from pessoas import views

urlpatterns = [
    path("pessoas/", views.PessoaListView.as_view(), name="listar-pessoas"),
    path(
        "pessoas/cadastrar/", views.PessoaCreateView.as_view(), name="cadastrar-pessoas"
    ),
    path("pessoas/<pk>/", views.PessoaUpdateView.as_view(), name="gerenciar-pessoa"),
    path(
        "pessoas/<pk>/deletar/",
        views.PessoaDeleteView.as_view(),
        name="deletar-pessoa",
    ),
    path(
        "templates/pessoas/",
        views.GetTemplatePessoas.as_view(),
        name="get-template-pessoas",
    ),
    path(
        "planilhas/pessoas/",
        views.PlanilhaPessoasView.as_view(),
        name="planilha-pessoas",
    ),
    path(
        "pessoas-estatisticas/",
        views.EstatisticasView.as_view(),
        name="estatisticas-pessoas",
    ),
]
