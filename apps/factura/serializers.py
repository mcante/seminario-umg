from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Factura, Ventas, Pedido, Despacho



# Rest Factura
class FacturaModelSerializer(serializers.ModelSerializer):
    cliente = serializers.StringRelatedField()
    vendedor = serializers.StringRelatedField(source = 'vendedor.get_full_name', default=None)
    estado_factura = serializers.StringRelatedField()
    estado_venta = serializers.StringRelatedField()

    fecha_factura = serializers.DateField(format="%d/%m/%Y") # Permite formatear la fecha
    
    class Meta:
        model = Factura
        fields = (  'id', 
                    'numero_factura', 
                    'cliente',
                    'pedido',
                    'fecha_factura',
                    'vendedor',
                    'estado_factura',
                    'estado_venta',
                    'completada',
                    'monto_total',
                    )

# Rest Ventas
class VentasModelSerializer(serializers.ModelSerializer):
    factura = serializers.StringRelatedField(source = 'factura.numero_factura', default=None)
    fecha_registro = serializers.DateField(format="%d/%m/%Y") # Permite formatear la fecha
    negocio = serializers.StringRelatedField(source = 'negocio.nombre_negocio', default=None)
    creado_por = serializers.StringRelatedField(source = 'creado_por.get_full_name', default=None)
    
    creado = serializers.DateTimeField(format="%d/%m/%Y  %H:%M:%S") # Permite formatear la fecha

    class Meta:
        model = Ventas
        fields = (  'id', 
                    'factura', 
                    'fecha_registro',
                    'monto_venta',
                    'negocio',
                    'creado_por',
                    'creado',
                    )



"""
    API DE CLIENTES PUBLICO
"""

# Rest Pedido
class PedidoModelSerializer(serializers.ModelSerializer):
    negocio = serializers.StringRelatedField(source = 'negocio.nombre_negocio', default=None)
    fecha_pedido = serializers.DateField(format="%d/%m/%Y") # Permite formatear la fecha
    vendedor = serializers.StringRelatedField(source = 'vendedor.get_full_name', default=None)
    estado_pedido = serializers.StringRelatedField(source = 'estado_pedido.nombre_estado', default=None)

    class Meta:
        model = Pedido
        fields = (  'id', 
                    'negocio',
                    'fecha_pedido',
                    'descripcion_detalle_pedido',
                    'vendedor',
                    'estado_pedido',
                    'anotaciones_seguimiento',
                    'completado',
                    )


# Rest Factura
class FacturaPublicoModelSerializer(serializers.ModelSerializer):
    cliente = serializers.StringRelatedField()
    vendedor = serializers.StringRelatedField(source = 'vendedor.get_full_name', default=None)
    estado_factura = serializers.StringRelatedField()
    estado_venta = serializers.StringRelatedField()

    fecha_factura = serializers.DateField(format="%d/%m/%Y") # Permite formatear la fecha
    
    class Meta:
        model = Factura
        fields = (  'id', 
                    'numero_factura', 
                    'cliente',
                    'pedido',
                    'fecha_factura',
                    'vendedor',
                    'estado_factura',
                    'estado_venta',
                    'completada',
                    'monto_total',
                    )



# Rest Despacho
class DespachoPublicoModelSerializer(serializers.ModelSerializer):
    factura = serializers.StringRelatedField(source = 'factura.numero_factura', default=None)
    empleado = serializers.StringRelatedField(source = 'empleado.get_full_name', default=None)
    estado_despacho = serializers.StringRelatedField()
    negocio = serializers.StringRelatedField(source = 'negocio.nombre_negocio', default=None)

    fecha_despacho = serializers.DateField(format="%d/%m/%Y") # Permite formatear la fecha
    
    class Meta:
        model = Despacho
        fields = (  'id', 
                    'factura', 
                    'fecha_despacho',
                    'persona_recibe',
                    'empleado',
                    'anotaciones_despacho',
                    'estado_despacho',
                    'negocio',
                    'completado'
                    )


"""
    ./API DE CLIENTES PUBLICO
"""