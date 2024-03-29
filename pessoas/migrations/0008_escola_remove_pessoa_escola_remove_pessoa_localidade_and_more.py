# Generated by Django 4.0.4 on 2022-09-24 20:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pessoas", "0007_alter_lideranca_options"),
    ]

    operations = [
        migrations.CreateModel(
            name="Escola",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "nome",
                    models.CharField(max_length=500, unique=True, verbose_name="Nome"),
                ),
                (
                    "localidade",
                    models.CharField(max_length=500, verbose_name="Localidade"),
                ),
            ],
            options={
                "ordering": ["nome"],
            },
        ),
        migrations.RemoveField(
            model_name="pessoa",
            name="escola",
        ),
        migrations.RemoveField(
            model_name="pessoa",
            name="localidade",
        ),
        migrations.CreateModel(
            name="Secao",
            fields=[
                ("id", models.IntegerField(primary_key=True, serialize=False)),
                (
                    "escola",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="secoes",
                        to="pessoas.escola",
                    ),
                ),
            ],
            options={
                "ordering": ["id"],
            },
        ),
        migrations.AlterField(
            model_name="pessoa",
            name="secao",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="pessoas",
                to="pessoas.secao",
            ),
        ),
    ]
