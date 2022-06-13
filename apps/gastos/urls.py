from django.urls import path

from .views import RegistroGastosCreateView, RegistroGastosUpdateView, \
RegistroGastosListAPIView, RegistroGastosFormView, RegistroGastosGlobalFormView

urlpatterns = [
    
    # Gastos
    path('add/', RegistroGastosCreateView.as_view(), name='gastos_add'),
    path('update/<int:pk>/', RegistroGastosUpdateView.as_view(), name='gastos_update'),

    # Registro de Compras
    path('api/gastos/filter/list/', RegistroGastosListAPIView.as_view(), name='gastos_filter_list_api'),
    path('filter/gastos/list/', RegistroGastosFormView.as_view(), name='gastos_filter_list'), # API con paginacion
    path('filter/gastos_global/list/', RegistroGastosGlobalFormView.as_view(), name='gastos_filter_global_list'), # API con paginacion

]