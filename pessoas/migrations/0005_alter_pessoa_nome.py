# Generated by Django 4.0.4 on 2022-09-21 00:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pessoas', '0004_alter_pessoa_escola_alter_pessoa_localidade_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='nome',
            field=models.CharField(max_length=500, unique=True, verbose_name='Nome'),
        ),
    ]