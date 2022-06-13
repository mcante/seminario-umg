from django.urls import path

from apps.registration.views import NegocioUsuarioTemplateView, NegocioUsuarioRetrieveUpdateDestroyAPIView, \
PresupuestoListView, PresupuestoCreateView, PresupuestoUpdateView, FinancieroTemplateView

urlpatterns = [
    
    # Switch Negocio
    path('accesos/', NegocioUsuarioTemplateView.as_view(), name='accesos_usuario_list'),

    # Presupuesto
    path('presupuestos/add/', PresupuestoCreateView.as_view(), name='presupuesto_add'),
    path('presupuestos/update/<int:pk>/', PresupuestoUpdateView.as_view(), name='presupuesto_update'),
    path('presupuesto/list/', PresupuestoListView.as_view(), name='presupuesto_list'),

    # Reporte del Estado Financiero Actual
    path('estado_financiero/', FinancieroTemplateView.as_view(), name='estado_financiero_view'),

    path('api/accesos/<int:pk>/', NegocioUsuarioRetrieveUpdateDestroyAPIView.as_view(), name='accesos_user_update_api'),

]