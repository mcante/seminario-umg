# Generated by Django 3.2.8 on 2022-06-04 10:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('planilla', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empleados',
            name='bonificacion_de_ley',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15, null=True, verbose_name='Bonificación de Ley'),
        ),
        migrations.AlterField(
            model_name='empleados',
            name='descuentos',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15, null=True, verbose_name='Descuentos'),
        ),
        migrations.AlterField(
            model_name='empleados',
            name='salario_base',
            field=models.DecimalField(blank=True, decimal_places=2, default=0.0, max_digits=15, null=True, verbose_name='Salario Base'),
        ),
    ]
