# Generated by Django 3.2.8 on 2022-05-26 22:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ventas_y_alquileres', '0005_auto_20220523_2153'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alquilermaquina',
            name='fecha_devolucion',
            field=models.DateField(blank=True, null=True, verbose_name='Fecha Prevista de Devolución'),
        ),
    ]
