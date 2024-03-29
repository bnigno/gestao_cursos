# Generated by Django 4.0.4 on 2022-09-23 17:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("pessoas", "0005_alter_pessoa_nome"),
    ]

    operations = [
        migrations.CreateModel(
            name="Lideranca",
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
            ],
        ),
        migrations.AddField(
            model_name="pessoa",
            name="lideranca",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="pessoas",
                to="pessoas.lideranca",
            ),
        ),
    ]
