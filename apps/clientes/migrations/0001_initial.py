# Generated by Django 3.2.8 on 2022-05-03 00:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('registration', '0002_auto_20220503_0035'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_empresa', models.CharField(blank=True, max_length=150, null=True, verbose_name='Nombre de la Empresa')),
                ('nombre_contacto', models.CharField(blank=True, max_length=150, null=True, verbose_name='Nombre del Contacto')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Correo')),
                ('telefono', models.IntegerField(blank=True, null=True, verbose_name='Teléfono')),
                ('extension', models.IntegerField(blank=True, null=True, verbose_name='Extensión')),
                ('nit', models.CharField(blank=True, max_length=150, null=True, verbose_name='Nit')),
                ('direccion', models.TextField(blank=True, null=True, verbose_name='Dirección')),
                ('key_access', models.CharField(blank=True, max_length=30, null=True, verbose_name='Llave de Acceso')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('actualizado', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('empleado_asignado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relClienteUser', to=settings.AUTH_USER_MODEL, verbose_name='Empleado Asignado')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Telefonos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero_telefono', models.IntegerField(blank=True, null=True, verbose_name='Número de Teléfono')),
                ('marcar_preferico', models.BooleanField(default=False, verbose_name='Marcar como preferido')),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relTelefonosCliente', to='clientes.cliente', verbose_name='Cliente')),
            ],
            options={
                'verbose_name': 'Teléfono',
                'verbose_name_plural': 'Teléfonos',
            },
        ),
        migrations.CreateModel(
            name='NegocioCliente',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relNegocioClienteCliente', to='clientes.cliente', verbose_name='Cliente')),
                ('negocio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relNegocioClienteNegocio', to='registration.negocio', verbose_name='Negocio')),
            ],
            options={
                'verbose_name': 'Asignar Negocio a Cliente',
                'verbose_name_plural': 'Asignar Negocio a Cliente',
                'ordering': ['-id'],
                'unique_together': {('negocio', 'cliente')},
            },
        ),
    ]
