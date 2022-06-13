# Generated by Django 3.2.8 on 2022-05-16 21:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('proveedores', '0001_initial'),
        ('plantas', '0005_delete_proveedor'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='proveedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relProductoProveedor', to='proveedores.proveedor', verbose_name='Proveedor'),
        ),
    ]
