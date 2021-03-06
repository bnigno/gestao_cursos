# Generated by Django 4.0.4 on 2022-05-16 15:49

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cursos', '0005_alter_aluno_cpf_alter_aluno_dados_pagamento_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='curso',
            name='carga_horaria',
            field=models.IntegerField(verbose_name='Carga Horária (h)'),
        ),
        migrations.AlterField(
            model_name='turma',
            name='valor_lanche',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Valor do lanche por dia'),
        ),
        migrations.AlterField(
            model_name='turma',
            name='valor_transporte',
            field=models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Valor do Transporte por aluno'),
        ),
    ]
