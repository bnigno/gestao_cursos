# Generated by Django 4.0.4 on 2022-05-15 15:08

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cursos', '0003_alter_professor_dados_pagamento'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='cpf',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='CPF'),
        ),
    ]