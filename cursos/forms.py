from django import forms

from .models import Professor, DadosPagamentos, Turma, Frequencia, FrequenciaAluno


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


class FrequenciaForm(forms.ModelForm):
    class Meta:
        model = Frequencia
        fields = "__all__"
        widgets = {
            'data': forms.HiddenInput(),
            'turma': forms.HiddenInput()
        }


class PresencaForm(forms.ModelForm):
    class Meta:
        model = FrequenciaAluno
        fields = '__all__'
        widgets = {
            'aluno': forms.HiddenInput(),
            'frequencia': forms.HiddenInput(),
            'presente': forms.CheckboxInput(attrs={'class': "form-check"})
        }

    def __init__(self, *args, **kwargs):
        super(PresencaForm, self).__init__(*args, **kwargs)
        if self.instance and self.instance.aluno:
            self.fields['presente'].label = f"&nbsp; {self.instance.aluno.nome}"


class DatasFrequenciaForm(forms.Form):
    data_list = forms.ChoiceField(label="Data", localize=True)

    def __init__(self, choices, *args, **kwargs):
        super(DatasFrequenciaForm, self).__init__(*args, **kwargs)
        self.fields['data_list'].choices = choices
