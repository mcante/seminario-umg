# Generated by Django 3.2.8 on 2022-05-16 20:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('registration', '0006_presupuesto'),
    ]

    operations = [
        migrations.CreateModel(
            name='Proveedor',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('actualizado', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('nombre_proveedor', models.CharField(blank=True, max_length=150, null=True, verbose_name='Nombre Proveedor')),
                ('nombre_contacto', models.CharField(blank=True, max_length=150, null=True, verbose_name='Nombre del Contacto')),
                ('telefono', models.IntegerField(blank=True, null=True, verbose_name='Teléfono')),
                ('nit', models.CharField(blank=True, max_length=150, null=True, verbose_name='Nit')),
                ('direccion', models.TextField(blank=True, null=True, verbose_name='Dirección')),
                ('negocio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relProveedoresNegocio', to='registration.negocio', verbose_name='Negocio')),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
                'ordering': ['-id'],
            },
        ),
    ]
