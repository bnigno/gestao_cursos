from django.db import models


class Municipio(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome")

    def __str__(self):
        return self.nome.capitalize()


class TiposPagamentos(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome")

    def __str__(self):
        return self.nome.capitalize()


class DadosPagamentos(models.Model):
    tipos_conta = [
        (1, 'Conta Corrente'),
        (2, 'Poupança'),
    ]
    tipo_pagamento = models.ForeignKey(TiposPagamentos, on_delete=models.CASCADE, verbose_name="Tipo de pagamento")
    chave_pix = models.CharField(max_length=300, blank=True, null=True, verbose_name="Chave PIX")
    banco = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nome do banco")
    agencia = models.CharField(max_length=50, blank=True, null=True, verbose_name="Agência bancária")
    conta = models.CharField(max_length=100, blank=True, null=True, verbose_name="Número da conta bancária")
    tipo_conta = models.IntegerField(choices=tipos_conta, blank=True, null=True, verbose_name="Tipo de conta bancária")


class Curso(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome")
    carga_horaria = models.IntegerField(verbose_name="Carga Horária (h)")

    def __str__(self):
        return self.nome.capitalize()


class Professor(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome")
    cpf = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name="CPF")
    dados_pagamento = models.OneToOneField(DadosPagamentos, null=True, blank=True, on_delete=models.PROTECT,
                                           verbose_name="Dados de pagamento")

    def __str__(self):
        return self.nome.capitalize()


class Aluno(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome")
    cpf = models.CharField(max_length=50, blank=True, null=True, unique=True, verbose_name="CPF")
    dados_pagamento = models.ForeignKey(DadosPagamentos, null=True, blank=True, on_delete=models.PROTECT,
                                        verbose_name="Dados de pagamento")

    def __str__(self):
        return self.nome.capitalize()


class Turma(models.Model):
    nome = models.CharField(max_length=200, verbose_name="Nome")
    curso = models.ForeignKey(Curso, on_delete=models.PROTECT, verbose_name="Curso")
    professor = models.ForeignKey(Professor, on_delete=models.PROTECT, verbose_name="Professor")
    municipio = models.ForeignKey(Municipio, on_delete=models.PROTECT, verbose_name="Município")
    dt_inicio = models.DateField(verbose_name="Data de inicio")
    dt_fim = models.DateField(verbose_name="Data de encerramento")
    valor_lanche = models.FloatField(verbose_name="Valor do lanche")
    valor_transporte = models.FloatField(verbose_name="Valor do Transporte")
    alunos = models.ManyToManyField(Aluno, related_name="turmas")

    def __str__(self):
        return self.nome.capitalize()


class Frequencia(models.Model):
    data = models.DateField(verbose_name="Data")
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, verbose_name="Turma")
    has_aula = models.BooleanField(verbose_name="Houve aula?", default=True)

    class Meta:
        unique_together = ["data", "turma"]

    def __str__(self):
        return f"{self.turma.nome} - {self.data.strftime('%d/%m/%Y')}"


class FrequenciaAluno(models.Model):
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name="frequencias")
    frequencia = models.ForeignKey(
        Frequencia, on_delete=models.CASCADE, related_name="alunos"
    )
    presente = models.BooleanField(help_text="O aluno estava presente?", default=True)

    class Meta:
        unique_together = ["aluno", "frequencia"]

    def __str__(self):
        return f"{self.frequencia} - {self.aluno} - {'Presente' if self.presente else 'Ausente'}"
