from django.urls import path

from .views import DispositivoGPSCreateView, DispositivoGPSUpdateView, DispositivoGPSListView, \
LogVelocidadesGPSListView, LogTiemposGPSListView, \
LogVelocidadesGPSListCreateAPIView, LogTiemposGPSListCreateAPIView, \
InventarioVehiculoCreateView, InventarioVehiculoUpdateView, InventarioVehiculoListView, \
AsignacionTarifaCreateView, AsignacionTarifaUpdateView, \
RutasCreateView, RutasUpdateView, FacturaCreateView, FacturaUpdateView, \
FichaSalidaCreateView, FichaSalidaUpdateView, FichaEntradaCreateView, FichaEntradaUpdateView, \
RutasLogPilotoUpdateView, LogRutaCreateView, RutasListView, RutasPilotoListView, \
FacturaFormView, FacturaTransporteView, InformeVelocidadRuta

urlpatterns = [
    
    # Dispositivo GPS
    path('dispositivo_gps/add/', DispositivoGPSCreateView.as_view(), name='dispositivo_gps_add'),
    path('dispositivo_gps/update/<int:pk>/', DispositivoGPSUpdateView.as_view(), name='dispositivo_gps_update'),
    path('dispositivo_gps/list/', DispositivoGPSListView.as_view(), name='dispositivogps_list'), # Con paginacion

    # Logs Dispositivos GPS
    path('log_velocidades_gps/list/<p_id_dispositivo>', LogVelocidadesGPSListView.as_view(), name='logs_velocidades_list'), # Con paginacion
    path('log_tiempos_gps/list/<p_id_dispositivo>', LogTiemposGPSListView.as_view(), name='logs_tiempos_list'), # Con paginacion


    # Inventario Vehiculo 
    path('inventario_vehiculo/add/', InventarioVehiculoCreateView.as_view(), name='inventario_vehiculo_add'),
    path('inventario_vehiculo/update/<int:pk>/', InventarioVehiculoUpdateView.as_view(), name='inventario_vehiculo_update'),
    path('inventario_vehiculo/list/', InventarioVehiculoListView.as_view(), name='inventario_vehiculo_list'), # Con paginacion

    # Asignación de Tarifas
    path('vehiculo_tarifa/add/', AsignacionTarifaCreateView.as_view(), name='vehiculo_tarifa_add'),
    path('vehiculo_tarifa/update/<int:pk>/', AsignacionTarifaUpdateView.as_view(), name='vehiculo_tarifa_update'),


    # Factura
    path('factura/add/', FacturaCreateView.as_view(), name='transportes_factura_add'),
    path('factura/update/<int:pk>/', FacturaUpdateView.as_view(), name='transportes_factura_update'),
    path('factura/pdf/<p_factura>/', FacturaTransporteView.as_view(), name='imprimir_factura_transportes_view'),

    # Rutas de Transporte
    path('ruta/add/', RutasCreateView.as_view(), name='ruta_add'),
    path('ruta/update/<int:pk>/', RutasUpdateView.as_view(), name='ruta_update'), # Admin
    path('ruta/list/', RutasListView.as_view(), name='rutas_list'), # Con paginacion
    path('ruta/informe/pdf/<p_ruta>/', InformeVelocidadRuta.as_view(), name='imprimir_ruta_informe_view'),

    path('ruta_piloto/update/<int:pk>/', RutasLogPilotoUpdateView.as_view(), name='ruta_piloto_update'), # Piloto Ruta
    path('ruta_piloto/log/add/', LogRutaCreateView.as_view(), name='ruta_piloto_log_add'), # Piloto Log
    path('ruta_piloto/list/', RutasPilotoListView.as_view(), name='rutas_piloto_list'), # Con paginacion

    # Ficha de Salida
    path('ruta/ficha_salida/add/', FichaSalidaCreateView.as_view(), name='ficha_salida_add'),
    path('ruta/ficha_salida/update/<int:pk>/', FichaSalidaUpdateView.as_view(), name='ficha_salida_update'),

    # Ficha de Entrada
    path('ruta/ficha_entrada/add/', FichaEntradaCreateView.as_view(), name='ficha_entrada_add'),
    path('ruta/ficha_entrada/update/<int:pk>/', FichaEntradaUpdateView.as_view(), name='ficha_entrada_update'),


    # REST
    path('api/log_velocidades_gps/', LogVelocidadesGPSListCreateAPIView.as_view(), name='api_logs_velocidades'),
    path('api/log_tiempos_gps/', LogTiemposGPSListCreateAPIView.as_view(), name='api_logs_tiempos'),

    path('ruta/filter/list/', FacturaFormView.as_view(), name='factura_transportes_filter_list'), # API con paginacion
    
]