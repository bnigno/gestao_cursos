# Generated by Django 4.0.4 on 2022-09-23 20:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pessoas', '0006_lideranca_pessoa_lideranca'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='lideranca',
            options={'ordering': ['nome']},
        ),
    ]