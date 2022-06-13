# Generated by Django 3.2.8 on 2022-05-03 00:16

import apps.registration.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre del Departamento')),
            ],
        ),
        migrations.CreateModel(
            name='GiroNegocio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('actualizado', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('nombre_giro', models.CharField(blank=True, max_length=150, null=True, verbose_name='Nombre del Giro de Negocio')),
                ('descripcion', models.TextField(blank=True, null=True, verbose_name='Descripción del Negocio')),
            ],
            options={
                'verbose_name': 'Giro de Negocio',
                'verbose_name_plural': 'Giros de Negocio',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Meses',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_mes', models.CharField(blank=True, max_length=50, null=True, verbose_name='Mes')),
            ],
            options={
                'verbose_name': 'Mes',
                'verbose_name_plural': 'Meses',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre del Municipio')),
                ('deparamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='relMunicipioDepartamento', to='registration.departamento', verbose_name='Departamento')),
            ],
        ),
        migrations.CreateModel(
            name='Negocio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('actualizado', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('nombre_negocio', models.CharField(blank=True, max_length=150, null=True, verbose_name='Nombre del Negocio')),
                ('telefono', models.IntegerField(blank=True, null=True, verbose_name='Teléfono')),
                ('extension', models.IntegerField(blank=True, null=True, verbose_name='Extensión')),
                ('email', models.EmailField(blank=True, max_length=254, null=True, verbose_name='Correo')),
                ('direccion', models.TextField(blank=True, null=True, verbose_name='Dirección')),
                ('giro_negocio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relNegocioGiroNegocio', to='registration.gironegocio', verbose_name='Giro de Negocio')),
                ('municipio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relNegocioMunicipio', to='registration.municipio', verbose_name='Municipio')),
            ],
            options={
                'verbose_name': 'negocio',
                'verbose_name_plural': 'negocios',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Pais',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre del País')),
            ],
        ),
        migrations.CreateModel(
            name='TipoPago',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre_tipo_pago', models.CharField(blank=True, max_length=100, null=True, verbose_name='Nombre del tipo de pago')),
            ],
            options={
                'verbose_name': 'Tipo de Pago',
                'verbose_name_plural': 'Tipos de Pago',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Salarios',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('actualizado', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('salario_base', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Salario Base')),
                ('bonificacion_de_ley', models.DecimalField(decimal_places=2, max_digits=6, verbose_name='Bonificación de Ley')),
                ('actualizado_pro', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relSalariosUserActualizadoPor', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado Por')),
                ('creado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relSalariosUserCreadoPor', to=settings.AUTH_USER_MODEL, verbose_name='Creado Por')),
                ('negocio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relSalariosNegocio', to='registration.negocio', verbose_name='Negocio')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relSalariosUser', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Salario',
                'verbose_name_plural': 'Salarios',
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Planilla',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('actualizado', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('salario', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Salario Base')),
                ('bonificacion_de_ley', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='Bonificación de Ley')),
                ('igss', models.DecimalField(blank=True, decimal_places=2, max_digits=6, null=True, verbose_name='IGSS')),
                ('actualizado_pro', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relPlanillaUserActualizadoPor', to=settings.AUTH_USER_MODEL, verbose_name='Actualizado Por')),
                ('creado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relPlanillaUserCreadoPor', to=settings.AUTH_USER_MODEL, verbose_name='Creado Por')),
                ('mes', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relPlanillaMeses', to='registration.meses', verbose_name='Planilla del Mes')),
                ('negocio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relPlanillaNegocio', to='registration.negocio', verbose_name='Negocio')),
                ('tipo_pago', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relPlanillaTipoPago', to='registration.tipopago', verbose_name='Tipo de Pago')),
                ('usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relPlanillaUser', to=settings.AUTH_USER_MODEL, verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Planilla',
                'verbose_name_plural': 'Planillas',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Perfil',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('actualizado', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to=apps.registration.models.elimina_imagen_cargada)),
                ('celular', models.IntegerField(blank=True, null=True, verbose_name='Celular')),
                ('activo', models.BooleanField(default=True)),
                ('negocio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relPerfilNegocio', to='registration.negocio', verbose_name='Negocio')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relPerfilUsuario', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'perfil',
                'verbose_name_plural': 'perfiles',
                'ordering': ['-user'],
            },
        ),
        migrations.AddField(
            model_name='departamento',
            name='pais',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relDepartamentoPais', to='registration.pais', verbose_name='País'),
        ),
        migrations.CreateModel(
            name='NegocioUsuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('creado', models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')),
                ('actualizado', models.DateTimeField(auto_now=True, verbose_name='Fecha de edición')),
                ('preferido', models.BooleanField(default=True)),
                ('negocio', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relNegocioUsuarioNegocio', to='registration.negocio', verbose_name='Negocio')),
                ('perfil_usuario', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='relNegocioUsuarioPerfil', to='registration.perfil', verbose_name='Usuario')),
            ],
            options={
                'verbose_name': 'Asignar Negocio',
                'verbose_name_plural': 'Asignar Negocio o Empresa',
                'ordering': ['-id'],
                'unique_together': {('negocio', 'perfil_usuario')},
            },
        ),
    ]
