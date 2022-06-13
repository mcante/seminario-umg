from django.urls import path

from .views import MaquinaCreateView, MaquinaUpdateView, MaquinaListView, \
InventarioMaquinariaVentasCreateView, InventarioMaquinariaVentasUpdateView, InventarioMaquinariaVentasListView, \
IngresoComprasCreateView, IngresoComprasUpdateView, IngresoComprasListView, \
InventarioMaquinariaAlquilerCreateView, InventarioMaquinariaAlquilerUpdateView, InventarioMaquinariaAlquilerListView, \
AlquilerMaquinaCreateView, AlquilerMaquinaUpdateView, AlquilerMaquinaListView, \
FacturaCreateView, FacturaUpdateView, DetalleFacturaCreateView, \
FacturaFormView, DetalleFacturaRetrieveUpdateDestroyAPIView, \
InventarioMaquinariaVentasListAPIView, InventarioMaquinariaAlquilerListAPIView, AlquilerMaquinaListAPIView, \
FacturaMaquinariaView

urlpatterns = [
    
    # Máquinas
    path('maquina/add/', MaquinaCreateView.as_view(), name='maquina_add'),
    path('maquina/update/<int:pk>/', MaquinaUpdateView.as_view(), name='maquina_update'),
    path('maquina/list/', MaquinaListView.as_view(), name='maquina_list'), # Con paginacion


    # Inventario Maquinaria Ventas
    path('inventario_ventas/add/', InventarioMaquinariaVentasCreateView.as_view(), name='inventario_ventas_add'),
    path('inventario_ventas/update/<int:pk>/', InventarioMaquinariaVentasUpdateView.as_view(), name='inventario_ventas_update'),
    path('inventario_ventas/list/', InventarioMaquinariaVentasListView.as_view(), name='inventario_ventas_list'), # Con paginacion

    # Ingreso Compras
    path('ingreso_inventario_compras/add/', IngresoComprasCreateView.as_view(), name='ingreso_inventario_compras_add'),
    path('ingreso_inventario_compras/update/<int:pk>/', IngresoComprasUpdateView.as_view(), name='ingreso_inventario_compras_update'),
    path('ingreso_inventario_compras/list/', IngresoComprasListView.as_view(), name='ingreso_inventario_compras_list'), # Con paginacion

    # Inventario de máquinas de Alquiler
    path('inventario_alquiler/add/', InventarioMaquinariaAlquilerCreateView.as_view(), name='inventario_alquiler_add'),
    path('inventario_alquiler/update/<int:pk>/', InventarioMaquinariaAlquilerUpdateView.as_view(), name='inventario_alquiler_update'),
    path('inventario_alquiler/list/', InventarioMaquinariaAlquilerListView.as_view(), name='inventario_alquiler_list'), # Con paginacion

    # Alquiler de maquinaria
    path('alquiler_maquina/add/', AlquilerMaquinaCreateView.as_view(), name='alquiler_maquina_add'),
    path('alquiler_maquina/update/<int:pk>/', AlquilerMaquinaUpdateView.as_view(), name='alquiler_maquina_update'),
    path('alquiler_maquina/list/', AlquilerMaquinaListView.as_view(), name='alquiler_maquina_list'), # Con paginacion

    # Factura
    path('factura/add/', FacturaCreateView.as_view(), name='maquinas_factura_add'),
    path('factura/update/<int:pk>/', FacturaUpdateView.as_view(), name='maquinas_factura_update'),
    path('factura/pdf/<p_factura>/', FacturaMaquinariaView.as_view(), name='imprimir_factura_maquinaria_view'),

    # Detalle Factura
    path('detalle_factura/add/', DetalleFacturaCreateView.as_view(), name='maquinas_detalle_factura_add'),    
    

    # REST
    path('factura/filter/list/', FacturaFormView.as_view(), name='factura_maquinas_filter_list'), # API con paginacion
    path('api/inventario_ventas/list/', InventarioMaquinariaVentasListAPIView.as_view(), name='inventario_ventas_list_api'), # Inventario Ventas
    path('api/inventario_alquiler/list/', InventarioMaquinariaAlquilerListAPIView.as_view(), name='inventario_alquiler_list_api'), # Inventario Alquiler
    path('api/ficha_alquiler/list/', AlquilerMaquinaListAPIView.as_view(), name='ficha_alquiler_list_api'), # Inventario Alquiler

    # Detalle Factura "quitar del detalle".
    path('api/factura_detalle/<int:pk>/', DetalleFacturaRetrieveUpdateDestroyAPIView.as_view(), name='factura_maquinas_detalle_api'),
    
]