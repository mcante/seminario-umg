# Generated by Django 3.2.8 on 2022-05-11 19:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0005_tipoempleado_negocio'),
        ('gastos', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='tipogasto',
            name='negocio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relTipoGastoNegocio', to='registration.negocio', verbose_name='Negocio'),
        ),
    ]
