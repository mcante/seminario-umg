from django.urls import path

from .views import ProyectoCreateView, ProyectoUpdateView, ProyectoListView, \
DocumentosCreateView, GastosProyectoCreateView, \
FacturaCreateView, FacturaUpdateView, DetalleFacturaEntregablesCreateView, \
FacturaFormView, FacturaConstructoraView

urlpatterns = [
    
    # Proyectos
    path('add/', ProyectoCreateView.as_view(), name='proyecto_add'),
    path('update/<int:pk>/', ProyectoUpdateView.as_view(), name='proyecto_update'),
    path('list/', ProyectoListView.as_view(), name='proyecto_list'), # Con paginacion

    # Documentos
    path('documento/add/', DocumentosCreateView.as_view(), name='documento_add'),
    #path('medida/update/<int:pk>/', MedidasUpdateView.as_view(), name='medida_update'),
    #path('medida/list/', MedidasListView.as_view(), name='medida_list'), # Con paginacion

    # Documentos
    path('gastos_proyecto/add/', GastosProyectoCreateView.as_view(), name='gastos_proyecto_add'),


    # Factura
    path('factura/add/', FacturaCreateView.as_view(), name='proyectos_factura_add'),
    path('factura/update/<int:pk>/', FacturaUpdateView.as_view(), name='proyectos_factura_update'),
    path('factura/pdf/<p_factura>/', FacturaConstructoraView.as_view(), name='imprimir_factura_constructora_view'),

    # Detalle Factura
    path('factura/detalle/add/', DetalleFacturaEntregablesCreateView.as_view(), name='proyectos_detalle_factura_add'),

    path('factura/filter/list/', FacturaFormView.as_view(), name='factura_proyectos_filter_list'), # API con paginacion
    
    
    # REST API
    #===============

    # Inventario
    #path('inventario_filter/list/', InventarioFormView.as_view(), name='productos_list'), # Con paginacion
    #path('api/inventario/list/', InventarioListAPIView.as_view(), name='inventario_list_api'),
    
    # Detalle Factura "quitar del detalle".
    #path('api/factura_detalle/<int:pk>/', DetalleFacturaRetrieveUpdateDestroyAPIView.as_view(), name='factura_detalle_api'),
    

    # Retorna tokens de authenticacion para REST API
    #path('api-token-auth/',views.obtain_auth_token,name='api-token-auth')
]