import django_filters
from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from .models import Inventario, DetalleFactura



# Filtro Inventario
class InventarioFilterSet(filters.FilterSet):

    class Meta:
        model = Inventario
        fields = ['producto', 'stock', 'negocio']
    

# Filtro DetalleFactura
class DetalleFacturaFilterSet(filters.FilterSet):

    class Meta:
        model = DetalleFactura
        fields = ['id', 'factura', 'negocio']
    
