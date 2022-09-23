from django import forms

from pessoas.models import Lideranca


class SendPlanilhaPessoaForm(forms.Form):
    arquivo = forms.FileField(widget=forms.FileInput(attrs={"accept": ".xlsx"}))
    lideranca = forms.ModelChoiceField(queryset=Lideranca.objects.all())
