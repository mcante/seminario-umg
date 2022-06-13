# Generated by Django 3.2.8 on 2022-05-04 23:39

import apps.plantas.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('registration', '0003_alter_negociousuario_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('factura', '0002_auto_20220504_2230'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoDespacho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_estado', models.CharField(blank=True, max_length=150, null=True, verbose_name='Estado del Despacho')),
            ],
            options={
                'verbose_name': 'Estado del Despacho',
                'verbose_name_plural': 'Estados de los Despachos',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Medidas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('medida', models.CharField(blank=True, max_length=150, null=True, verbose_name='Unidad de Medida')),
            ],
            options={
                'verbose_name': 'Medida',
                'verbose_name_plural': 'Medidas',
                'ordering': ['-id'],
            },
        ),
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
                ('negocio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relProveedorNegocio', to='registration.negocio', verbose_name='Negocio')),
            ],
            options={
                'verbose_name': 'Proveedor',
                'verbose_name_plural': 'Proveedores',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('actualizado', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('nombre', models.CharField(blank=True, max_length=150, null=True, verbose_name='Nombre del Producto')),
                ('descripcion', models.CharField(blank=True, max_length=150, null=True, verbose_name='Descripción')),
                ('imagen_producto', models.ImageField(blank=True, null=True, upload_to=apps.plantas.models.fn_elimina_imagen_cargada)),
                ('actualizado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relProductoUpdateUser', to=settings.AUTH_USER_MODEL)),
                ('creado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relProductoCreateUser', to=settings.AUTH_USER_MODEL)),
                ('negocio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relProductoNegocio', to='registration.negocio', verbose_name='Negocio')),
                ('proveedor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relProductoProveedor', to='plantas.proveedor', verbose_name='Proveedor')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Inventario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('actualizado', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Precio Producto')),
                ('stock', models.IntegerField(blank=True, null=True, verbose_name='Stock')),
                ('actualizado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relInventarioPlantaUpdateUser', to=settings.AUTH_USER_MODEL)),
                ('creado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relInventarioPlantaCreateUser', to=settings.AUTH_USER_MODEL)),
                ('negocio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relInventarioPlantaNegocio', to='registration.negocio', verbose_name='Negocio')),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relInventarioProducto', to='plantas.producto', verbose_name='Producto')),
                ('unidad_medida', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relInventarioFactura', to='plantas.medidas', verbose_name='Unidad de Medida')),
            ],
            options={
                'verbose_name': 'Inventario',
                'verbose_name_plural': 'Inventario',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='DetalleFactura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('actualizado', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('cantidad', models.IntegerField(blank=True, null=True, verbose_name='Cantidad')),
                ('precio', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Precio Producto')),
                ('actualizado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relDetalleFacturaPlantaUpdateUser', to=settings.AUTH_USER_MODEL)),
                ('creado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relDetalleFacturaPlantaCreateUser', to=settings.AUTH_USER_MODEL)),
                ('factura', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relDetalleFacturaFactura', to='factura.factura', verbose_name='Factura')),
                ('negocio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relDetalleFacturaPlantaNegocio', to='registration.negocio', verbose_name='Negocio')),
                ('producto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relDetalleFacturaProducto', to='plantas.producto', verbose_name='Producto')),
            ],
            options={
                'verbose_name': 'Detalle de Factura',
                'verbose_name_plural': 'Detalle de Facturas',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Despacho',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('actualizado', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('fecha_despacho', models.DateField(verbose_name='Fecha del Despacho')),
                ('persona_recibe', models.CharField(blank=True, max_length=150, null=True, verbose_name='Persona que Recibe')),
                ('anotaciones_despacho', models.TextField(blank=True, null=True, verbose_name='Anotaciones del Despacho')),
                ('completado', models.BooleanField(default=False)),
                ('actualizado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relDespachoUpdateUser', to=settings.AUTH_USER_MODEL)),
                ('creado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relDespachoCreateUser', to=settings.AUTH_USER_MODEL)),
                ('empleado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relDespachoUserEmpleado', to=settings.AUTH_USER_MODEL, verbose_name='Empleado Entrega')),
                ('estado_despacho', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relDespachoEstadoDespacho', to='plantas.estadodespacho', verbose_name='Estado del Despacho')),
                ('factura', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relDespachoFactura', to='factura.factura', verbose_name='Factura')),
                ('negocio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relDespachoNegocio', to='registration.negocio', verbose_name='Negocio')),
            ],
            options={
                'verbose_name': 'Despacho',
                'verbose_name_plural': 'Despachos',
                'ordering': ['-id'],
            },
        ),
    ]