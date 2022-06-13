from django.urls import path

from apps.mensajeria import views as v_mensajeria

urlpatterns = [
    
    # Encabezado de Mensajeria
    path('encabezado/add/', v_mensajeria.EncabezadoMensajeCreateView.as_view(), name='mensajeria_encabezado_add'),
    path('encabezado/update/<int:pk>/', v_mensajeria.EncabezadoMensajeUpdateView.as_view(), name='mensajeria_encabezado_update'),
    path('encabezado/list/', v_mensajeria.EncabezadoMensajeListView.as_view(), name='mensajeria_encabezado_list'),

    # Hilo de Mensajes | Mensajeria
    path('mensaje/add/', v_mensajeria.HiloMensajeCreateView.as_view(), name='mensajeria_mensaje_add'),
    path('mensaje/update/<int:pk>/', v_mensajeria.HiloMensajeUpdateView.as_view(), name='mensajeria_mensaje_update'),
    
]