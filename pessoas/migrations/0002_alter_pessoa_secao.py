# Generated by Django 4.0.4 on 2022-09-21 00:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pessoas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='secao',
            field=models.IntegerField(null=True, verbose_name='Seção'),
        ),
    ]
