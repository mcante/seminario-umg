# Generated by Django 3.2.8 on 2022-05-23 20:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ventas_y_alquileres', '0002_auto_20220522_2232'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingresocompras',
            options={'ordering': ['-id'], 'verbose_name': 'Ingreso de Compras', 'verbose_name_plural': 'Ingreso de Compras'},
        ),
        migrations.RemoveField(
            model_name='ingresocompras',
            name='tipo_maquina',
        ),
        migrations.RemoveField(
            model_name='inventariomaquinariaventas',
            name='tipo_maquina',
        ),
    ]