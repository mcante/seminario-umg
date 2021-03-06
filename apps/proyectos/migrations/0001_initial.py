# Generated by Django 3.2.8 on 2022-05-16 23:15

import apps.proyectos.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('registration', '0006_presupuesto'),
        ('factura', '0005_alter_factura_monto_total'),
        ('clientes', '0002_negociocliente_vendedor'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TipoProyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=150, null=True, verbose_name='Tipo de Proyecto')),
            ],
            options={
                'verbose_name': 'Tipo de Proyecto',
                'verbose_name_plural': 'Tipos de Proyecto',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Proyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('actualizado', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('nombre_proyecto', models.CharField(blank=True, max_length=250, null=True, verbose_name='Nombre del Proyecto')),
                ('fecha_inicio', models.DateField(verbose_name='Fecha de Inicio')),
                ('fecha_fin', models.DateField(verbose_name='Fecha de Inicio')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción del Proyecto')),
                ('presupuesto_estimado', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Presupuesto Estimado')),
                ('gastos_totales', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Gastos Totales')),
                ('completado', models.BooleanField(default=False)),
                ('actualizado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relProyectoUpdateUser', to=settings.AUTH_USER_MODEL)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relProyectoCliente', to='clientes.cliente', verbose_name='Cliente')),
                ('creado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relProyectoCreateUser', to=settings.AUTH_USER_MODEL)),
                ('empleado', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relProyectoUserEmpleado', to=settings.AUTH_USER_MODEL, verbose_name='Empleado Asignado')),
                ('negocio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relProyectoNegocio', to='registration.negocio', verbose_name='Negocio')),
                ('tipo_proyecto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relProyectoTipoProyecto', to='proyectos.tipoproyecto', verbose_name='Tipo Proyecto')),
            ],
            options={
                'verbose_name': 'Proyecto',
                'verbose_name_plural': 'Proyectos',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='GastosProyecto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('actualizado', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('titulo_gasto', models.CharField(blank=True, max_length=150, null=True, verbose_name='Título del Gasto')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('fecha_gasto', models.DateField(verbose_name='Fecha de Gasto')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Monto')),
                ('documento_adjunto', models.ImageField(blank=True, null=True, upload_to=apps.proyectos.models.fn_elimina_imagen_cargada_gastos)),
                ('actualizado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relGastosProyectoUpdateUser', to=settings.AUTH_USER_MODEL)),
                ('autorizado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relGastosProyectoUserEmpleado', to=settings.AUTH_USER_MODEL, verbose_name='Autorizado Por')),
                ('creado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relGastosProyectoCreateUser', to=settings.AUTH_USER_MODEL)),
                ('negocio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relGastosProyectoNegocio', to='registration.negocio', verbose_name='Negocio')),
                ('proyecto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relGastosProyectoProyecto', to='proyectos.proyecto', verbose_name='Proyecto')),
            ],
            options={
                'verbose_name': 'Gasto del Proyecto',
                'verbose_name_plural': 'Gastos del Proyecto',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Documentos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('actualizado', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('titulo_documento', models.CharField(blank=True, max_length=150, null=True, verbose_name='Título del Documento')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción')),
                ('documento_adjunto', models.ImageField(blank=True, null=True, upload_to=apps.proyectos.models.fn_elimina_imagen_cargada)),
                ('actualizado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relDocumentosUpdateUser', to=settings.AUTH_USER_MODEL)),
                ('creado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relDocumentosCreateUser', to=settings.AUTH_USER_MODEL)),
                ('proyecto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relDocumentosProyecto', to='proyectos.proyecto', verbose_name='Proyecto')),
            ],
            options={
                'verbose_name': 'Documento',
                'verbose_name_plural': 'Documentos',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='DetalleFacturaEntregables',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('actualizado', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('fecha_entregable', models.DateField(verbose_name='Fecha del Entregable')),
                ('monto', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Monto')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción del Entregable')),
                ('actualizado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relDetalleFacturaEntregablesUpdateUser', to=settings.AUTH_USER_MODEL)),
                ('creado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relDetalleFacturaEntregablesCreateUser', to=settings.AUTH_USER_MODEL)),
                ('factura', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relFacturaProyecto', to='factura.factura', verbose_name='Factura')),
                ('negocio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relDetalleFacturaEntregablesNegocio', to='registration.negocio', verbose_name='Negocio')),
                ('proyecto', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relDetalleFacturaEntregablesProyecto', to='proyectos.proyecto', verbose_name='Proyecto')),
            ],
            options={
                'verbose_name': 'Gasto del Proyecto',
                'verbose_name_plural': 'Gastos del Proyecto',
                'ordering': ['-id'],
            },
        ),
    ]
