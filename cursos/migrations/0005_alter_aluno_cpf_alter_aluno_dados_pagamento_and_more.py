# Generated by Django 4.0.4 on 2022-05-15 23:31

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('cursos', '0004_alter_professor_cpf'),
    ]

    operations = [
        migrations.AlterField(
            model_name='aluno',
            name='cpf',
            field=models.CharField(blank=True, max_length=50, null=True, unique=True, verbose_name='CPF'),
        ),
        migrations.AlterField(
            model_name='aluno',
            name='dados_pagamento',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                    to='cursos.dadospagamentos', verbose_name='Dados de pagamento'),
        ),
        migrations.AlterField(
            model_name='dadospagamentos',
            name='agencia',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Agência bancária'),
        ),
        migrations.AlterField(
            model_name='dadospagamentos',
            name='banco',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Nome do banco'),
        ),
        migrations.AlterField(
            model_name='dadospagamentos',
            name='chave_pix',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='Chave PIX'),
        ),
        migrations.AlterField(
            model_name='dadospagamentos',
            name='conta',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Número da conta bancária'),
        ),
        migrations.AlterField(
            model_name='dadospagamentos',
            name='tipo_conta',
            field=models.IntegerField(blank=True, choices=[(1, 'Conta Corrente'), (2, 'Poupança')], null=True,
                                      verbose_name='Tipo de conta bancária'),
        ),
        migrations.AlterField(
            model_name='professor',
            name='dados_pagamento',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT,
                                       to='cursos.dadospagamentos', verbose_name='Dados de pagamento'),
        ),
    ]
