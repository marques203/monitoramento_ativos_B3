# Generated by Django 5.1.2 on 2024-10-26 18:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_inoa', '0002_alter_ativo_table_alter_usuario_table'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='ativo',
            table='ativos',
        ),
        migrations.AlterModelTable(
            name='usuario',
            table='usuarios',
        ),
    ]
