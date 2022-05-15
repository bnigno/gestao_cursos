# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

from django.urls import path

from cursos import views

urlpatterns = [

    # The home page
    path('', views.index, name='home'),
    path('professores/', views.ProfessorListView.as_view(), name='listar-professores'),
    path('professores/cadastrar/', views.ProfessorCreateView.as_view(), name='cadastrar-professores'),
    path('professores/<pk>/', views.ProfessorUpdateView.as_view(), name='gerenciar-professor'),
    path('professores/<pk>/deletar/', views.ProfessorDeleteView.as_view(), name='deletar-professor'),

]
