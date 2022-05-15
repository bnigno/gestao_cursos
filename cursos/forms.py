from django import forms

from .models import Professor, DadosPagamentos


class ProfessorForm(forms.ModelForm):
    class Meta:
        model = Professor
        fields = ('nome', 'cpf',)


class DadosPagamentosForm(forms.ModelForm):
    class Meta:
        model = DadosPagamentos
        fields = '__all__'