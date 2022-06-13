from django.urls import path

from .views import ProveedorCreateView, ProveedorUpdateView, ProveedorListView, \
MedidasCreateView, MedidasUpdateView, MedidasListView, \
ProductoCreateView, ProductoUpdateView, ProductoListView, \
InventarioListAPIView, InventarioFormView, InventarioCreateView, InventarioUpdateView, \
FacturaCreateView, FacturaUpdateView, DetalleFacturaCreateView, \
DetalleFacturaRetrieveUpdateDestroyAPIView, \
FacturaFormView, \
IngresoComprasCreateView, IngresoComprasUpdateView, IngresoComprasListView, \
FacturaPlantaView

urlpatterns = [
    
    # Proveedores
    path('proveedor/add/', ProveedorCreateView.as_view(), name='proveedor_add'),
    path('proveedor/update/<int:pk>/', ProveedorUpdateView.as_view(), name='proveedor_update'),
    path('proveedor/list/', ProveedorListView.as_view(), name='proveedor_list'), # Con paginacion

    # Medidas
    path('medida/add/', MedidasCreateView.as_view(), name='medida_add'),
    path('medida/update/<int:pk>/', MedidasUpdateView.as_view(), name='medida_update'),
    path('medida/list/', MedidasListView.as_view(), name='medida_list'), # Con paginacion

    # Producto
    path('producto/add/', ProductoCreateView.as_view(), name='producto_add'),
    path('producto/update/<int:pk>/', ProductoUpdateView.as_view(), name='producto_update'),
    path('productos/list/', ProductoListView.as_view(), name='productos_list'), # Con paginacion
    
    # Inventario
    path('inventario/add/', InventarioCreateView.as_view(), name='inventario_add'),
    path('inventario/update/<int:pk>/', InventarioUpdateView.as_view(), name='inventario_update'),

    # Ingreso Compras
    path('ingreso_inventario_compras/add/', IngresoComprasCreateView.as_view(), name='plantas_ingreso_inventario_compras_add'),
    path('ingreso_inventario_compras/update/<int:pk>/', IngresoComprasUpdateView.as_view(), name='plantas_ingreso_inventario_compras_update'),
    path('ingreso_inventario_compras/list/', IngresoComprasListView.as_view(), name='plantas_ingreso_inventario_compras_list'), # Con paginacion

    # Factura
    path('factura/add/', FacturaCreateView.as_view(), name='planta_factura_add'),
    path('factura/update/<int:pk>/', FacturaUpdateView.as_view(), name='planta_factura_update'),
    path('factura/pdf/<p_factura>/', FacturaPlantaView.as_view(), name='imprimir_factura_planta_view'),

    # Detalle Factura
    path('factura/detalle/add/', DetalleFacturaCreateView.as_view(), name='planta_detalle_factura_add'),

    
    # REST API
    #===============

    # Factura
    path('filter/list/', FacturaFormView.as_view(), name='plantas_factura_filter_list'), # API con paginacion

    # Inventario
    path('inventario_filter/list/', InventarioFormView.as_view(), name='plantas_inventario_list'), # Con paginacion
    path('api/inventario/list/', InventarioListAPIView.as_view(), name='plantas_inventario_list_api'),
    
    # Detalle Factura "quitar del detalle".
    path('api/factura_detalle/<int:pk>/', DetalleFacturaRetrieveUpdateDestroyAPIView.as_view(), name='factura_detalle_api'),
    

    # Retorna tokens de authenticacion para REST API
    #path('api-token-auth/',views.obtain_auth_token,name='api-token-auth')
]