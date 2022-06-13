# Generated by Django 3.2.8 on 2022-05-12 20:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plantas', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='inventario',
            name='unidad_medida',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relInventarioMedidas', to='plantas.medidas', verbose_name='Unidad de Medida'),
        ),
    ]