from django import forms

from .models import Professor, DadosPagamentos, Turma


class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ('nome', 'cpf',)


class DadosPagamentosForm(forms.ModelForm):
    class Meta:
        model = DadosPagamentos
        fields = ('tipo_pagamento', 'chave_pix', 'banco', 'agencia', 'conta', 'tipo_conta')


class TurmaForm(forms.ModelForm):
    class Meta:
        model = Turma
        fields = (
        'curso', 'municipio', 'dt_inicio', 'dt_fim', 'professor', 'valor_lanche', 'valor_transporte', 'alunos')
        widgets = {
            'dt_inicio': forms.DateInput(attrs={'type': "date"}),
            'dt_fim': forms.DateInput(attrs={'type': "date"})
        }
