# Generated by Django 3.2.8 on 2022-05-04 20:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('registration', '0002_auto_20220503_0035'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='negociousuario',
            options={'ordering': ['-id'], 'verbose_name': 'Asignar Negocio a Usuario', 'verbose_name_plural': 'Asignar Negocio a Usuario'},
        ),
    ]
