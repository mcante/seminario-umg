# Generated by Django 3.2.8 on 2022-05-22 22:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas_y_alquileres', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='maquina',
            name='nombre',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Nombre Máquina'),
        ),
        migrations.AlterField(
            model_name='maquina',
            name='descripcion',
            field=models.CharField(blank=True, max_length=250, null=True, verbose_name='Descripción'),
        ),
    ]