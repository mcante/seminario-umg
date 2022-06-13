from django.urls import path

from .views import PedidoAdminCreateView, PedidoAdminUpdateView, PedidoListView, \
FacturaCreateView, FacturaAdminUpdateView, FacturaListAPIView, FacturaFormView, \
VentasListAPIView, VentasFormView, VentasGlobalFormView, \
PedidoGeneralListView, DespachoCreateView, DespachoUpdateView, DespachoListView, \
PedidoListAPIView, PedidoDetailView, \
FacturaPublicoListAPIView, FacturaPublicoDetailView, \
DespachoPublicoListAPIView, DespachoPublicoDetailView


urlpatterns = [
    
    # Pedidos
    path('pedido/add/', PedidoAdminCreateView.as_view(), name='pedido_add'),
    path('pedido/update/<int:pk>/', PedidoAdminUpdateView.as_view(), name='pedido_update'),
    path('pedido/user_list/', PedidoListView.as_view(), name='pedido_user_list'),
    path('pedido/general_list/', PedidoGeneralListView.as_view(), name='pedido_general_list'),

    # Factura
    path('add/', FacturaCreateView.as_view(), name='factura_add'),
    path('update/<int:pk>/', FacturaAdminUpdateView.as_view(), name='factura_update'),

    # Despacho
    path('despacho/add/', DespachoCreateView.as_view(), name='despacho_add'),
    path('despacho/update/<int:pk>/', DespachoUpdateView.as_view(), name='despacho_update'),
    path('despacho/list/', DespachoListView.as_view(), name='despacho_list'),

    #path('negocio_cliente/add/', NegocioClienteCreateView.as_view(), name='negocio_cliente_add'),
    
    # REST API
    #path('api/negocio_cliente/<int:pk>/', NegocioClienteRetrieveUpdateDestroyAPIView.as_view(), name='negocio_cliente_api'),
    #path('api/list/', ClienteListAPIView.as_view(), name='clientes_list_filter_api'), # API con paginacion
    
    # Factura
    path('api/filter/list/', FacturaListAPIView.as_view(), name='factura_filter_list_api'), # API con paginacion
    path('filter/list/', FacturaFormView.as_view(), name='factura_filter_list'), # API con paginacion

    # Ventas
    path('api/ventas/filter/list/', VentasListAPIView.as_view(), name='ventas_filter_list_api'), # API con paginacion
    path('filter/ventas/list/', VentasFormView.as_view(), name='ventas_filter_list'), # API con paginacion
    path('filter/ventas_gloal/list/', VentasGlobalFormView.as_view(), name='ventas_filter_global_list'), # API con paginacion
    

    # Clientes PEDIDO publico
    path('api/clientes_pedido/filter/list/', PedidoListAPIView.as_view(), name='clientes_pedido_filter_list_api'), # API con paginacion
    path('cliente/pedidos/<llave>/<int:pk>/', PedidoDetailView.as_view(), name='clientes_pedido_list'),

    # Clientes FACTURAS publico
    path('api/clientes_factura/filter/list/', FacturaPublicoListAPIView.as_view(), name='clientes_factura_filter_list_api'), # API con paginacion
    path('cliente/facturas/<llave>/<int:pk>/', FacturaPublicoDetailView.as_view(), name='clientes_factura_list'),

    # Clientes DESPACHO publico
    path('api/clientes_despacho/filter/list/', DespachoPublicoListAPIView.as_view(), name='clientes_despacho_filter_list_api'), # API con paginacion
    path('cliente/despachos/<llave>/<int:pk>/', DespachoPublicoDetailView.as_view(), name='clientes_despacho_list'),


]