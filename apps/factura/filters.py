import django_filters
from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from .models import Factura, Ventas, Pedido, Despacho



# Filtro Factura
class FacturaFilterSet(filters.FilterSet):

    # Filtro para buscar por un rango de fechas según la fecha de la factura
    fecha_factura_min = django_filters.DateFilter(field_name='fecha_factura_min', method='filter_fecha_factura')
    fecha_factura_max = django_filters.DateFilter(field_name='fecha_factura_max', method='filter_fecha_factura')
    
    class Meta:
        model = Factura
        fields = ['id', 'numero_factura', 'cliente', 'fecha_factura', 'vendedor', 'estado_factura', 'estado_venta', 'completada', 'negocio']
    
    # fecha_boleta
    def filter_fecha_factura(self, queryset, field_name, value):
        if value and field_name == 'fecha_factura_min':
            queryset = queryset.filter(fecha_factura__gte=value)
        if value and field_name == 'fecha_factura_max':
            queryset = queryset.filter(fecha_factura__lte=value)
        return queryset



# Filtro Ventas
class VentasFilterSet(filters.FilterSet):

    # Filtro para buscar por un rango de fechas según la fecha de la boleta
    fecha_registro_min = django_filters.DateFilter(field_name='fecha_registro_min', method='filter_fecha_registro')
    fecha_registro_max = django_filters.DateFilter(field_name='fecha_registro_max', method='filter_fecha_registro')
    
    class Meta:
        model = Ventas
        fields = ['id', 'fecha_registro', 'negocio']
    
    # fecha_boleta
    def filter_fecha_registro(self, queryset, field_name, value):
        if value and field_name == 'fecha_registro_min':
            queryset = queryset.filter(fecha_registro__gte=value)
        if value and field_name == 'fecha_registro_max':
            queryset = queryset.filter(fecha_registro__lte=value)
        return queryset






"""
    API DE CLIENTES PUBLICO
"""

# Filtro Pedido
class PedidoFilterSet(filters.FilterSet):

    # Filtro para buscar por un rango de fechas según la fecha de la boleta
    fecha_pedido_min = django_filters.DateFilter(field_name='fecha_pedido_min', method='filter_fecha_pedido')
    fecha_pedido_max = django_filters.DateFilter(field_name='fecha_pedido_max', method='filter_fecha_pedido')
    
    class Meta:
        model = Pedido
        fields = ['id', 'cliente', 'fecha_pedido', 'negocio', 'completado']
    
    # fecha_boleta
    def filter_fecha_pedido(self, queryset, field_name, value):
        if value and field_name == 'fecha_pedido_min':
            queryset = queryset.filter(fecha_pedido__gte=value)
        if value and field_name == 'fecha_pedido_max':
            queryset = queryset.filter(fecha_pedido__lte=value)
        return queryset



# Filtro Factura
class FacturaPublicoFilterSet(filters.FilterSet):

    # Filtro para buscar por un rango de fechas según la fecha de la factura
    fecha_factura_min = django_filters.DateFilter(field_name='fecha_factura_min', method='filter_fecha_factura')
    fecha_factura_max = django_filters.DateFilter(field_name='fecha_factura_max', method='filter_fecha_factura')
    
    class Meta:
        model = Factura
        fields = ['id', 'numero_factura', 'cliente', 'fecha_factura', 'vendedor', 'estado_factura', 'estado_venta', 'completada', 'negocio']
    
    # fecha_boleta
    def filter_fecha_factura(self, queryset, field_name, value):
        if value and field_name == 'fecha_factura_min':
            queryset = queryset.filter(fecha_factura__gte=value)
        if value and field_name == 'fecha_factura_max':
            queryset = queryset.filter(fecha_factura__lte=value)
        return queryset




# Filtro Despacho
class DespachoPublicoFilterSet(filters.FilterSet):

    # Filtro para buscar por un rango de fechas según la fecha de la factura
    fecha_despacho_min = django_filters.DateFilter(field_name='fecha_despacho_min', method='filter_fecha_despacho')
    fecha_despacho_max = django_filters.DateFilter(field_name='fecha_despacho_max', method='filter_fecha_despacho')
    
    class Meta:
        model = Despacho
        fields = ['id', 'factura', 'fecha_despacho', 'persona_recibe', 'empleado', 'estado_despacho', 'negocio', 'completado', 'factura__cliente']
    
    # fecha_boleta
    def filter_fecha_despacho(self, queryset, field_name, value):
        if value and field_name == 'fecha_despacho_min':
            queryset = queryset.filter(fecha_despacho__gte=value)
        if value and field_name == 'fecha_despacho_max':
            queryset = queryset.filter(fecha_despacho__lte=value)
        return queryset


"""
    ./API DE CLIENTES PUBLICO
"""