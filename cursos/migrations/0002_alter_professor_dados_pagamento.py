# Generated by Django 4.0.4 on 2022-05-12 23:47

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cursos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='professor',
            name='dados_pagamento',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='cursos.dadospagamentos',
                                    verbose_name='Dados de pagamento'),
        ),
    ]
