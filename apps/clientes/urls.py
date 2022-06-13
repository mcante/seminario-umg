from django.urls import path

from .views import PrincipalTemplateView, \
ClienteCreateView, ClienteUpdateView, NegocioClienteCreateView, \
NegocioClienteRetrieveUpdateDestroyAPIView, ClienteListAPIView, ClienteFormView, \
InicioTemplateView, AcercaDeTemplateView, ContactoTemplateView, PedidosTemplateView, \
PedidoPublicCreateView, PedidosSuccessTemplateView, AccesoClientesTemplateView, \
ClientePublicListAPIView, NegocioClientePublicListAPIView, \
PerfilClienteDetailView, ContactoPublicCreateView, ContactoSuccessTemplateView, \
ContactoUpdateView, ContactoListView, \
PlantaInventarioListView, PlantaTransformacionesInventarioListView, TransporteInventarioListView, \
MaquinariaInventarioListView

urlpatterns = [
    # Sitio web público
    path('', InicioTemplateView.as_view(), name='inicio_view'),
    path('acerca/', AcercaDeTemplateView.as_view(), name='acerca_de_view'),
    #path('contacto/', ContactoTemplateView.as_view(), name='contacto_view'),
    path('contacto/', ContactoPublicCreateView.as_view(), name='contacto_view'),
    path('contacto/success/', ContactoSuccessTemplateView.as_view(), name='contacto_satisfactorio_view'),
    path('pedidos/', PedidosTemplateView.as_view(), name='pedidos_view'),
    path('pedidos/success/', PedidosSuccessTemplateView.as_view(), name='pedidos_satisfactorio_view'),
    path('cliente/acceso/', AccesoClientesTemplateView.as_view(), name='acceso_clientes_view'),

    # Contacto Admin
    path('contacto/list/', ContactoListView.as_view(), name='contacto_list'),
    path('contacto/update/<int:pk>/', ContactoUpdateView.as_view(), name='contacto_update'),

    # PROMOCIÓN DE PRODUCTOS
    path('minera/list/', PlantaInventarioListView.as_view(), name='minera_list'),
    path('transformaciones/list/', PlantaTransformacionesInventarioListView.as_view(), name='transformaciones_list'),
    path('transportes/list/', TransporteInventarioListView.as_view(), name='transportes_list'),
    path('maquinaria/list/', MaquinariaInventarioListView.as_view(), name='maquinaria_list'),
    
    # Acceso con llave cliente
    path('cliente/principal/<llave>/<int:pk>/', PerfilClienteDetailView.as_view(), name='cliente_principal_view'),

    # Pedidos
    path('pedidos/add/', PedidoPublicCreateView.as_view(), name='cliente_pedido_add'),

    # Principal Sistema
    path('dashboard/', PrincipalTemplateView.as_view(), name='principal_view'),

    # Clientes
    path('add/', ClienteCreateView.as_view(), name='cliente_add'),
    path('update/<int:pk>/', ClienteUpdateView.as_view(), name='cliente_update'),
    path('negocio_cliente/add/', NegocioClienteCreateView.as_view(), name='negocio_cliente_add'),

    # REST API
    path('api/negocio_cliente/<int:pk>/', NegocioClienteRetrieveUpdateDestroyAPIView.as_view(), name='negocio_cliente_api'),
    path('api/list/', ClienteListAPIView.as_view(), name='clientes_list_filter_api'), # API con paginacion
    
    path('filter/list/', ClienteFormView.as_view(), name='cliente_filter_list'), # API con paginacion

    # Cliente buscar llave
    path('api/filter_key/', ClientePublicListAPIView.as_view(), name='clientes_filter_key_api'), 
    path('api/negocio_cliente/list/', NegocioClientePublicListAPIView.as_view(), name='negocio_cliente_list_api'), 
    

    # Retorna tokens de authenticacion para REST API
    #path('api-token-auth/',views.obtain_auth_token,name='api-token-auth')
]