# Generated by Django 5.1.2 on 2024-10-26 19:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_inoa', '0004_ativo_valor_maximo_ativo_valor_minimo_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ativo',
            name='valor',
        ),
        migrations.AddField(
            model_name='ativo',
            name='periodo_checagem',
            field=models.IntegerField(default=5, validators=[django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='ativo',
            name='valor_maximo',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
        migrations.AlterField(
            model_name='ativo',
            name='valor_minimo',
            field=models.DecimalField(decimal_places=2, max_digits=10, validators=[django.core.validators.MinValueValidator(0)]),
        ),
    ]
