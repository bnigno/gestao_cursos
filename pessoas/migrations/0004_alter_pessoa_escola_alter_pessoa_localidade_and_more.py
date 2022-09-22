# Generated by Django 4.0.4 on 2022-09-21 00:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pessoas', '0003_alter_pessoa_localidade'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pessoa',
            name='escola',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Escola'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='localidade',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='Localidade'),
        ),
        migrations.AlterField(
            model_name='pessoa',
            name='secao',
            field=models.IntegerField(blank=True, null=True, verbose_name='Seção'),
        ),
    ]
