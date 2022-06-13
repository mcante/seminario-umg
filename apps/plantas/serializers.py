from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Inventario, DetalleFactura



# Rest Inventario
class InventarioModelSerializer(serializers.ModelSerializer):
    producto = serializers.StringRelatedField(source = 'producto.nombre', default=None)
    unidad_medida = serializers.StringRelatedField(source = 'unidad_medida.medida', default=None)
    negocio = serializers.StringRelatedField(source = 'negocio.nombre_negocio', default=None)
    creado_por = serializers.StringRelatedField(source = 'creado_por.get_full_name', default=None)
    
    class Meta:
        model = Inventario
        fields = (  'id', 
                    'producto', 
                    'precio',
                    'stock',
                    'unidad_medida',
                    'negocio',
                    'creado_por',
                    )



# Rest DetalleFactura
class DetalleFacturaModelSerializer(serializers.ModelSerializer):
    factura = serializers.StringRelatedField(default=None)
    producto = serializers.StringRelatedField(source = 'producto.nombre', default=None)
    negocio = serializers.StringRelatedField(source = 'negocio.nombre_negocio', default=None)
    creado_por = serializers.StringRelatedField(source = 'creado_por.get_full_name', default=None)
    
    class Meta:
        model = DetalleFactura
        fields = (  'id', 
                    'factura', 
                    'producto',
                    'cantidad',
                    'precio',
                    'negocio',
                    'creado_por',
                    )