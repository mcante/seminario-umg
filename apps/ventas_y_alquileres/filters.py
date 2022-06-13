import django_filters
from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from .models import InventarioMaquinariaVentas, InventarioMaquinariaAlquiler, AlquilerMaquina, DetalleFactura



# Filtro InventarioMaquinariaVentas
class InventarioMaquinariaVentasFilterSet(filters.FilterSet):

    class Meta:
        model = InventarioMaquinariaVentas
        fields = ['id', 'maquina', 'stock', 'negocio']

# VENTAS
# Filtro InventarioMaquinariaAlquiler
class InventarioMaquinariaAlquilerFilterSet(filters.FilterSet):

    class Meta:
        model = InventarioMaquinariaAlquiler
        fields = ['id', 'maquina', 'disponible', 'negocio']

# ALQUILER
# Filtro AlquilerMaquina
class AlquilerMaquinaFilterSet(filters.FilterSet):

    class Meta:
        model = AlquilerMaquina
        fields = ['id', 'maquina_alquiler', 'estado_alquiler', 'devuelto', 'negocio']


# Filtro DetalleFactura
class DetalleFacturaFilterSet(filters.FilterSet):

    class Meta:
        model = DetalleFactura
        fields = ['id', 'factura', 'negocio']
    
