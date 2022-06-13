# Generated by Django 3.2.8 on 2022-06-04 15:57

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0008_auto_20220603_2132'),
        ('mensajeria', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='hilomensaje',
            name='negocio_destino',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relHiloMensajeDestinoNegocio', to='registration.negocio', verbose_name='Negocio Destino'),
        ),
    ]
