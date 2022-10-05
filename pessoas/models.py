from django.db import models


class Lideranca(models.Model):
    nome = models.CharField(max_length=500, verbose_name="Nome", unique=True)

    def __str__(self):
        return self.nome

    class Meta:
        ordering = ["nome"]


class Escola(models.Model):
    nome = models.CharField(max_length=500, verbose_name="Nome", unique=True)
    localidade = models.CharField(max_length=500, verbose_name="Localidade")

    def __str__(self):
        return f"{self.nome} - {self.localidade}"

    class Meta:
        ordering = ["nome"]


class Secao(models.Model):
    id = models.IntegerField(primary_key=True)
    escola = models.ForeignKey(
        Escola, on_delete=models.SET_NULL, related_name="secoes", null=True
    )

    def __str__(self):
        return str(self.id)

    class Meta:
        ordering = ["id"]


class Pessoa(models.Model):
    nome = models.CharField(max_length=500, verbose_name="Nome", unique=True)
    zona = models.IntegerField(verbose_name="Zona", default=78)
    secao = models.ForeignKey(
        Secao, on_delete=models.SET_NULL, related_name="pessoas", null=True, blank=True
    )
    lideranca = models.ForeignKey(
        Lideranca, on_delete=models.SET_NULL, related_name="pessoas", null=True
    )
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nome


class Postulante(models.Model):
    nome = models.CharField(max_length=500, verbose_name="Nome", unique=True)


class Resultado(models.Model):
    secao = models.ForeignKey(
        Secao, on_delete=models.CASCADE, related_name="resultado", verbose_name="Seção"
    )
    quantidade = models.IntegerField(verbose_name="Quantidade")
    postulante = models.ForeignKey(
        Postulante,
        on_delete=models.CASCADE,
        related_name="resultado",
        verbose_name="Postulante",
    )
