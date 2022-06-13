import django_filters
from django_filters import rest_framework as filters
from django.contrib.auth.models import User
from .models import TipoGasto, RegistroGastos




# Filtro RegistroGastos
class RegistroGastosFilterSet(filters.FilterSet):

    # Filtro para buscar por un rango de fechas según la fecha del gasto
    fecha_gasto_min = django_filters.DateFilter(field_name='fecha_gasto_min', method='filter_fecha_gasto')
    fecha_gasto_max = django_filters.DateFilter(field_name='fecha_gasto_max', method='filter_fecha_gasto')
    
    class Meta:
        model = RegistroGastos
        fields = ['id', 'tipo_gasto', 'fecha_gasto', 'autorizado_por', 'negocio']
    
    def filter_fecha_gasto(self, queryset, field_name, value):
        if value and field_name == 'fecha_gasto_min':
            queryset = queryset.filter(fecha_gasto__gte=value)
        if value and field_name == 'fecha_gasto_max':
            queryset = queryset.filter(fecha_gasto__lte=value)
        return queryset