from rest_framework import serializers
from django.contrib.auth.models import User

from .models import InventarioMaquinariaVentas, InventarioMaquinariaAlquiler, AlquilerMaquina, DetalleFactura



# Rest InventarioMaquinariaVentas para detalle Factura
class InventarioMaquinariaVentasModelSerializer(serializers.ModelSerializer):
    maquina = serializers.StringRelatedField(source = 'maquina.nombre', default=None)
    negocio = serializers.StringRelatedField(source = 'negocio.nombre_negocio', default=None)
    creado_por = serializers.StringRelatedField(source = 'creado_por.get_full_name', default=None)
    
    class Meta:
        model = InventarioMaquinariaVentas
        fields = (  'id', 
                    'maquina', 
                    'precio',
                    'stock',
                    'negocio',
                    'creado_por',
                    )

# INVENTARIO ALQUILER
# Rest InventarioMaquinariaAlquiler para detalle Factura
class InventarioMaquinariaAlquilerModelSerializer(serializers.ModelSerializer):
    maquina = serializers.StringRelatedField(source = 'maquina.nombre', default=None)
    negocio = serializers.StringRelatedField(source = 'negocio.nombre_negocio', default=None)
    creado_por = serializers.StringRelatedField(source = 'creado_por.get_full_name', default=None)
    
    class Meta:
        model = InventarioMaquinariaAlquiler
        fields = (  'id', 
                    'maquina', 
                    'precio_por_dia',
                    'disponible',
                    'negocio',
                    'creado_por',
                    )

# FICHA ALQUILER
# Rest AlquilerMaquina para detalle Factura
class AlquilerMaquinaModelSerializer(serializers.ModelSerializer):
    maquina_alquiler = serializers.StringRelatedField(source = 'maquina_alquiler.maquina.nombre', default=None)
    estado_alquiler = serializers.StringRelatedField(source = 'estado_alquiler.estado_alquiler', default=None)
    negocio = serializers.StringRelatedField(source = 'negocio.nombre_negocio', default=None)
    creado_por = serializers.StringRelatedField(source = 'creado_por.get_full_name', default=None)
    
    class Meta:
        model = AlquilerMaquina
        fields = (  'id', 
                    'maquina_alquiler', 
                    'fecha_entrega',
                    'fecha_devolucion',
                    'estado_alquiler',
                    'devuelto',
                    'fn_calcular_dias',
                    'negocio',
                    'creado_por',
                    )



# Rest DetalleFactura
class DetalleFacturaModelSerializer(serializers.ModelSerializer):
    factura = serializers.StringRelatedField(default=None)
    negocio = serializers.StringRelatedField(source = 'negocio.nombre_negocio', default=None)
    creado_por = serializers.StringRelatedField(source = 'creado_por.get_full_name', default=None)
    
    class Meta:
        model = DetalleFactura
        fields = (  'id', 
                    'factura', 
                    'cantidad',
                    'precio',
                    'negocio',
                    'creado_por',
                    )