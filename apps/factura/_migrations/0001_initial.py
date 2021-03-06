# Generated by Django 3.2.8 on 2022-05-02 20:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clientes', '0002_auto_20220502_1803'),
        ('registration', '0003_auto_20220502_1754'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadoFactura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_estado', models.CharField(blank=True, max_length=150, null=True, verbose_name='Estado de Factura')),
            ],
        ),
        migrations.CreateModel(
            name='EstadoVenta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_estado_venta', models.CharField(blank=True, max_length=150, null=True, verbose_name='Estado de la Venta')),
            ],
        ),
        migrations.CreateModel(
            name='Factura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('actualizado', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('numero_factura', models.IntegerField(blank=True, null=True, verbose_name='Número Factura')),
                ('fecha_factura', models.DateField(verbose_name='Fecha de la Factura')),
                ('monto_total', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Monto Facturado')),
                ('completada', models.BooleanField(default=False)),
                ('actualizado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relFacturaUpdateUser', to=settings.AUTH_USER_MODEL)),
                ('cliente', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relFacturaCliente', to='clientes.cliente', verbose_name='Cliente')),
                ('creado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relFacturaCreateUser', to=settings.AUTH_USER_MODEL)),
                ('estado_factura', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relFacturaEstadoFactura', to='factura.estadofactura', verbose_name='Estado Factura')),
                ('estado_venta', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relFacturaEstadoVenta', to='factura.estadoventa', verbose_name='Estado de la Venta')),
                ('sede', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relFacturaSede', to='registration.sede', verbose_name='Sede')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='TipoPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_tipo_pago', models.CharField(blank=True, max_length=150, null=True, verbose_name='Tipo de Pago')),
            ],
        ),
        migrations.CreateModel(
            name='Ventas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('actualizado', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('fecha_registro', models.DateField(verbose_name='Fecha de Registro')),
                ('monto_venta', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Monto Venta')),
                ('actualizado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relVentasUpdateUser', to=settings.AUTH_USER_MODEL)),
                ('creado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relVentasCreateUser', to=settings.AUTH_USER_MODEL)),
                ('factura', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relVentasFactura', to='factura.factura', verbose_name='Factura')),
                ('sede', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relVentasSede', to='registration.sede', verbose_name='Sede')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='factura',
            name='tipo_pago',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relFacturaTipoPago', to='factura.tipopago', verbose_name='Tipo de Pago'),
        ),
        migrations.AddField(
            model_name='factura',
            name='vendedor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relFacturaUserVendedor', to=settings.AUTH_USER_MODEL, verbose_name='Vendedor Asignado'),
        ),
        migrations.CreateModel(
            name='CorrelativoFactura',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('actualizado', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('correlativo', models.IntegerField(verbose_name='Correlativo Factura')),
                ('nomenclatura', models.CharField(max_length=15, verbose_name='Nomenclatura Sede')),
                ('sede', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relCorrelativoFacturaSede', to='registration.sede', verbose_name='Sede')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
