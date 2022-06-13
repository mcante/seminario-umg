# Generated by Django 3.2.8 on 2022-05-25 22:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factura', '0006_alter_factura_monto_total'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='monto_total',
            field=models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=13, null=True, verbose_name='Monto Facturado'),
        ),
    ]
