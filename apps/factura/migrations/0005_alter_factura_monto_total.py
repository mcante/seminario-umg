# Generated by Django 3.2.8 on 2022-05-14 00:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('factura', '0004_auto_20220508_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='factura',
            name='monto_total',
            field=models.DecimalField(blank=True, decimal_places=2, default='0.00', max_digits=6, null=True, verbose_name='Monto Facturado'),
        ),
    ]
