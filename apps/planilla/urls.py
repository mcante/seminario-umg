from django.urls import path

from apps.planilla import views as v_planilla

urlpatterns = [
    
    # Empleado
    path('empleado/add/', v_planilla.EmpleadosCreateView.as_view(), name='empleado_add'),
    path('empleado/update/<int:pk>/', v_planilla.EmpleadosUpdateView.as_view(), name='empleado_update'),
    path('empleado/list/', v_planilla.EmpleadosListView.as_view(), name='empleado_list'),

    # Encabezado de Planillas
    path('encabezado_planilla/add/', v_planilla.EncabezadoPlanillaCreateView.as_view(), name='encabezado_add'),
    path('encabezado_planilla/update/<int:pk>/', v_planilla.EncabezadoPlanillaUpdateView.as_view(), name='encabezado_update'),
    path('encabezado_planilla/list/', v_planilla.EncabezadoPlanillaListView.as_view(), name='encabezado_list'),

    # Cuerpo de Planillas
    path('cuerpo_planilla/add/', v_planilla.PlanillaCreateView.as_view(), name='cuerpo_planilla_add'),
    path('cuerpo_planilla/update/<int:pk>/', v_planilla.PlanillaUpdateView.as_view(), name='cuerpo_planilla_update'),
    
]