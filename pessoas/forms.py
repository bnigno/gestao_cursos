from django import forms


class SendPlanilhaPessoaForm(forms.Form):
    arquivo = forms.FileField(widget=forms.FileInput(attrs={"accept": ".xlsx"}))
    # lideranca = forms.ModelChoiceField(
    #     queryset=Lideranca.objects.order_by("nome").all()
    # )
