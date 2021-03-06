# Generated by Django 3.2.8 on 2022-05-28 21:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0006_presupuesto'),
        ('factura', '0008_auto_20220526_2208'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='descripcion_detalle_pedido',
            field=models.TextField(blank=True, null=True, verbose_name='Detalle del Pedido'),
        ),
        migrations.AlterField(
            model_name='pedido',
            name='negocio',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relPedidoNegocio', to='registration.negocio', verbose_name='Categoría de Negocio'),
        ),
    ]
