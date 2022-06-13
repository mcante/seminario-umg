from rest_framework import serializers
from django.contrib.auth.models import User
from .models import TipoGasto, RegistroGastos



# Rest RegistroGastos
class RegistroGastosModelSerializer(serializers.ModelSerializer):
    tipo_gasto = serializers.StringRelatedField(source = 'tipo_gasto.nombre_gasto', default=None)
    autorizado_por = serializers.StringRelatedField(source = 'autorizado_por.get_full_name', default=None)
    negocio = serializers.StringRelatedField(source = 'negocio.nombre_negocio', default=None)

    fecha_gasto = serializers.DateField(format="%d/%m/%Y") # Permite formatear la fecha
    
    class Meta:
        model = RegistroGastos
        fields = (  'id', 
                    'tipo_gasto', 
                    'fecha_gasto',
                    'monto',
                    'autorizado_por',
                    'negocio',
                    )
