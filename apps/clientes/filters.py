import django_filters
from django_filters import rest_framework as filters
from .models import NegocioCliente, Cliente


# Filtro NegocioCliente
class NegocioClienteFilterSet(filters.FilterSet):
    
    class Meta:
        model = NegocioCliente
        fields = ['id', 'cliente', 'negocio']



# Filtro Cliente
class ClienteFilterSet(filters.FilterSet):
    
    class Meta:
        model = Cliente
        fields = ['id', 'nombre_empresa', 'email', 'telefono', 'nit', 'empleado_asignado', 'relNegocioClienteCliente__negocio']


# Filtro Cliente Publico
class ClientePublicFilterSet(filters.FilterSet):
    
    class Meta:
        model = Cliente
        fields = ['id', 'key_access', 'email', 'telefono', 'nit', 'empleado_asignado', 'relNegocioClienteCliente__negocio']


# Filtro NegocioCliente Publico
class NegocioClientePublicFilterSet(filters.FilterSet):
    
    class Meta:
        model = NegocioCliente
        fields = ['id', 'cliente', 'negocio']
