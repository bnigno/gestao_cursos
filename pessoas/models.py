from django.db import models


class Lideranca(models.Model):
    nome = models.CharField(max_length=500, verbose_name="Nome", unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ["nome"]


class Pessoa(models.Model):
    nome = models.CharField(max_length=500, verbose_name="Nome", unique=True)
    zona = models.IntegerField(verbose_name="Zona")
    secao = models.IntegerField(verbose_name="Seção", null=True, blank=True)
    escola = models.CharField(
        max_length=200, verbose_name="Escola", null=True, blank=True
    )
    localidade = models.CharField(
        max_length=100, verbose_name="Localidade", null=True, blank=True
    )
    lideranca = models.ForeignKey(
        Lideranca, on_delete=models.SET_NULL, related_name="pessoas", null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome
