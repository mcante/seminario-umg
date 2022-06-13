#import pdb; pdb.set_trace()
from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from django.views.generic import UpdateView, DetailView, ListView, CreateView, FormView, TemplateView, View
from django.urls import reverse_lazy, reverse
from django.db.models import Avg, Max, Sum, Min, Count

import datetime
from django.utils import timezone

# Configuración del settings, variables
from django.conf import settings

# Decoradores para validar permisos de autenticación y grupos
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin

# Modelos
from .models import Marca, Linea, TipoVehiculo, TransmisionVehiculo, \
DispositivoGPS, LogVelocidadesGPS, LogTiemposGPS, InventarioVehiculo, AsignacionTarifa, \
Rutas, TipoLog, LogRuta, FichaSalida, FichaEntrada

from apps.factura.models import Factura

# Formulario compartido de FACTURAS
from apps.factura.forms import FacturaRestForm

# Formularios
from .forms import DispositivoGPSForm, InventarioVehiculoCreateForm, AsignacionTarifaCreateForm,\
RutasCreateForm, FacturaCreateForm, RutasLogPilotoUpdateForm, LogRutaCreateForm, FacturaUpdateForm, \
FichaSalidaCreateForm, FichaEntradaCreateForm


# REST
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.permissions import AllowAny

# Serializadores y filtros para REST
from .serializers import LogVelocidadesGPSModelSerializer, LogTiemposGPSModelSerializer
#from .filters import InventarioFilterSet, DetalleFacturaFilterSet


# Render personalizado para pdf
from apps.factura.htmltopdf import render_to_pdf

""" DispositivoGPS """

# DispositivoGPS | Agregar
class DispositivoGPSCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Operativo"]
    model = DispositivoGPS
    form_class = DispositivoGPSForm
    template_name = 'transportes/dispositivogps_add.html'

    def get_success_url(self):
        return reverse('dispositivo_gps_update', kwargs={'pk':self.object.id})



# 1.2. Actualizar DispositivoGPS
class DispositivoGPSUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Operativo"]
    model = DispositivoGPS
    form_class = DispositivoGPSForm
    template_name = 'transportes/dispositivogps_add.html'

    def get_success_url(self):
        return reverse('dispositivo_gps_update', kwargs={'pk':self.object.id})



# Lista los DispositivoGPS
class DispositivoGPSListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Operativo"]
    model = DispositivoGPS
    paginate_by = 100
    template_name = 'transportes/dispositivogps_list.html'




# LOGS LOGS DEBEN DE HACERSE EN UN REPORTE CON FORMULAS MATEMATICAS
# Lista los LogVelocidadesGPS
class LogVelocidadesGPSListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Supervisor", u"Operativo"]
    model = LogVelocidadesGPS
    paginate_by = 100
    template_name = 'transportes/log_velocidad_gps_list.html'

    def get_queryset(self, *args, **kwargs):
        lv_dispositivo = self.kwargs.get('p_id_dispositivo',None)
        queryset = super(LogVelocidadesGPSListView, self).get_queryset()
        return queryset.filter(dispositivo_gps=lv_dispositivo)


# Lista los LogTiemposGPS
class LogTiemposGPSListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Supervisor", u"Operativo"]
    model = LogTiemposGPS
    paginate_by = 100
    template_name = 'transportes/log_tiempos_gps_list.html'

    def get_queryset(self, *args, **kwargs):
        lv_dispositivo = self.kwargs.get('p_id_dispositivo',None)
        queryset = super(LogTiemposGPSListView, self).get_queryset()
        return queryset.filter(dispositivo_gps=lv_dispositivo)


""" ./ DispositivoGPS """






""" Vehiculos """


# InventarioVehiculo | Agregar
class InventarioVehiculoCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Contador", u"Operativo"]
    model = InventarioVehiculo
    form_class = InventarioVehiculoCreateForm
    template_name = 'transportes/inventario_vehiculo_add.html'

    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'negocio':lv_negocio, 'creado_por':self.request.user}

    def get_success_url(self):
        return reverse('inventario_vehiculo_update', kwargs={'pk':self.object.id})

# InventarioVehiculo | Actualizar
class InventarioVehiculoUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Contador", u"Operativo"]
    model = InventarioVehiculo
    form_class = InventarioVehiculoCreateForm
    template_name = 'transportes/inventario_vehiculo_update.html'

    def get_context_data(self, **kwargs):
        context = super(InventarioVehiculoUpdateView, self).get_context_data(**kwargs)

        context['tarifas_list'] = AsignacionTarifa.objects.filter(vehiculo=self.object)

        # Agrega el formulario para el añadir tarifas
        context['asignar_tarifa_form'] = AsignacionTarifaCreateForm(initial={
                                                        'vehiculo':self.object
                                                        })

        return context

    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'actualizado_por':self.request.user}

    def get_success_url(self):
        return reverse('inventario_vehiculo_update', kwargs={'pk':self.object.id})



# Lista los InventarioVehiculo
class InventarioVehiculoListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Contador", u"Operativo", u"Vendedor"]
    model = InventarioVehiculo
    paginate_by = 100
    template_name = 'transportes/inventario_vehiculos_list.html'



""" ./ Vehiculos """





""" AsignacionTarifa """


# AsignacionTarifa | Agregar
class AsignacionTarifaCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Operativo", u"Contador"]
    model = AsignacionTarifa
    form_class = AsignacionTarifaCreateForm
    template_name = 'transportes/asignacion_tarifa_add.html'

    def get_success_url(self):
        return reverse('inventario_vehiculo_update', kwargs={'pk':self.object.vehiculo.id})


# AsignacionTarifa | Actualizar
class AsignacionTarifaUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Operativo", u"Contador"]
    model = AsignacionTarifa
    form_class = AsignacionTarifaCreateForm
    template_name = 'transportes/asignacion_tarifa_add.html'

    def get_success_url(self):
        return reverse('inventario_vehiculo_update', kwargs={'pk':self.object.vehiculo.id})


""" ./ AsignacionTarifa """





"""
    FACTURA
    ------------------
"""
# Factura | Agregar
class FacturaCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Operativo", u"Vendedor"]
    model = Factura
    form_class = FacturaCreateForm
    template_name = 'transportes/factura_add.html'


    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'negocio':lv_negocio, 'creado_por':self.request.user}


    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(FacturaCreateView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs
    
    
    def get_success_url(self):
        if(self.object.pedido):
            return reverse('pedido_update', kwargs={'pk':self.object.pedido.id}) # Si se crea desde pedido, regresa a Pedido
        else:
            return reverse('transportes_factura_update', kwargs={'pk':self.object.id}) # Sino tiene pedido, se redirecciona a la factura





# Factura | Actualizar
class FacturaUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Operativo", u"Vendedor"]
    model = Factura
    form_class = FacturaUpdateForm
    template_name = 'transportes/factura_update.html'

    def get_context_data(self, **kwargs):
        context = super(FacturaUpdateView, self).get_context_data(**kwargs)
        
        context['detalle_factura_list'] = Rutas.objects.filter(factura = self.object)
        

        # Agrega un formulario y lo pasa al contexto.
        p_negocio = self.request.user.relPerfilUsuario.negocio

        context['detalle_factura_form'] = RutasCreateForm(p_negocio, initial={
                                                        'factura':self.object,
                                                        'creado_por':self.request.user,
                                                        'negocio':p_negocio
                                                        })
        
        return context
    

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(FacturaUpdateView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs
    
    
    def get_success_url(self):
        return reverse('transportes_factura_update', kwargs={'pk':self.object.id})



"""
    ./FACTURA
    ------------------
"""






""" Rutas """


# Rutas | Agregar
class RutasCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Operativo", u"Operativo", u"Vendedor"]
    model = Rutas
    form_class = RutasCreateForm
    template_name = 'transportes/ruta_add.html'

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(RutasCreateView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs

    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'negocio':lv_negocio, 'creado_por':self.request.user}

    def get_success_url(self):
        return reverse('transportes_factura_update', kwargs={'pk':self.object.factura.id})


# Rutas | Actualizar
class RutasUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Operativo", u"Operativo", u"Vendedor", u"Piloto"]
    model = Rutas
    form_class = RutasCreateForm
    template_name = 'transportes/ruta_update.html'

    def get_context_data(self, **kwargs):
        context = super(RutasUpdateView, self).get_context_data(**kwargs)
        
        context['ficha_salida_list'] = FichaSalida.objects.filter(ruta = self.object)
        context['ficha_entrada_list'] = FichaEntrada.objects.filter(ruta = self.object)
        

        # Agrega un formulario y lo pasa al contexto.
        p_negocio = self.request.user.relPerfilUsuario.negocio

        context['ficha_salida_form'] = FichaSalidaCreateForm(p_negocio, initial={
                                                        'ruta':self.object
                                                        })
        
        context['ficha_entrada_form'] = FichaEntradaCreateForm(p_negocio, initial={
                                                        'ruta':self.object
                                                        })
        
        return context

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(RutasUpdateView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs

    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'negocio':lv_negocio, 'actualizado_por':self.request.user}

    def get_success_url(self):
        return reverse('transportes_factura_update', kwargs={'pk':self.object.factura.id})







# Rutas LOG Piloto | Actualizar
class RutasLogPilotoUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Operativo", u"Vendedor", u"Piloto"]
    model = Rutas
    form_class = RutasLogPilotoUpdateForm
    template_name = 'transportes/ruta_piloto_update.html'

    def get_context_data(self, **kwargs):
        context = super(RutasLogPilotoUpdateView, self).get_context_data(**kwargs)
        
        context['log_ruta_list'] = LogRuta.objects.filter(ruta = self.object)

        # Agrega un formulario y lo pasa al contexto.
        #p_negocio = self.request.user.relPerfilUsuario.negocio

        context['log_ruta_form'] = LogRutaCreateForm(initial={
                                                        'ruta':self.object,
                                                        'negocio':self.object.negocio,
                                                        'fecha_hora_log':datetime.datetime.now(),
                                                        'creado_por':self.request.user
                                                        })
        
        return context

    def get_success_url(self):
        return reverse('ruta_piloto_update', kwargs={'pk':self.object.id})




# LogRuta | Agregar
class LogRutaCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Operativo", u"Piloto"]
    model = LogRuta
    form_class = LogRutaCreateForm
    template_name = 'transportes/ruta_log_piloto_add.html'

    def get_success_url(self):
        return reverse('ruta_piloto_update', kwargs={'pk':self.object.ruta.id})




# Lista los Rutas
class RutasListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Operativo", u"Vendedor", u"Piloto"]
    model = Rutas
    paginate_by = 100
    template_name = 'transportes/rutas_list.html'



# Lista las Rutas
class RutasPilotoListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Piloto"]
    model = Rutas
    paginate_by = 100
    template_name = 'transportes/rutas_piloto_list.html'

    def get_queryset(self, *args, **kwargs):
        
        queryset = super(RutasPilotoListView, self).get_queryset()
        return queryset.filter(piloto=self.request.user, completada=False)




""" Rutas """





""" FichaSalida """


# FichaSalida | Agregar
class FichaSalidaCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Operativo", u"Vendedor", u"Piloto"]
    model = FichaSalida
    form_class = FichaSalidaCreateForm
    template_name = 'transportes/ficha_salida_add.html'

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(FichaSalidaCreateView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs

    def get_success_url(self):
        return reverse('ruta_update', kwargs={'pk':self.object.ruta.id})


# FichaSalida | Actualizar
class FichaSalidaUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Operativo", u"Vendedor", u"Piloto"]
    model = FichaSalida
    form_class = FichaSalidaCreateForm
    template_name = 'transportes/ficha_salida_add.html'

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(FichaSalidaUpdateView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs

    def get_success_url(self):
        return reverse('ruta_update', kwargs={'pk':self.object.ruta.id})


""" FichaSalida """






""" FichaEntrada """


# FichaEntrada | Agregar
class FichaEntradaCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Operativo", u"Vendedor", u"Piloto"]
    model = FichaEntrada
    form_class = FichaEntradaCreateForm
    template_name = 'transportes/ficha_entrada_add.html'

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(FichaEntradaCreateView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs

    def get_success_url(self):
        return reverse('ruta_update', kwargs={'pk':self.object.ruta.id})


# FichaEntrada | Actualizar
class FichaEntradaUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Operativo", u"Vendedor", u"Piloto"]
    model = FichaEntrada
    form_class = FichaEntradaCreateForm
    template_name = 'transportes/ficha_entrada_add.html'

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(FichaEntradaUpdateView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs

    def get_success_url(self):
        return reverse('ruta_update', kwargs={'pk':self.object.ruta.id})


""" FichaEntrada """








"""
    REST
"""



# Para agregar log de velocidades al GPS
# 1.1: Representa el API, Utiliza el Serializer y el Filtro.
class LogVelocidadesGPSListCreateAPIView(ListCreateAPIView):
    serializer_class = LogVelocidadesGPSModelSerializer
    queryset = LogVelocidadesGPS.objects.all()
    #filter_class = LogVelocidadesGPSFilterSet


# Para agregar log de tiempos al GPS
# 1.1: Representa el API, Utiliza el Serializer y el Filtro.
class LogTiemposGPSListCreateAPIView(ListCreateAPIView):
    serializer_class = LogTiemposGPSModelSerializer
    queryset = LogTiemposGPS.objects.all()
    #filter_class = LogTiemposGPSFilterSet


# Formulario compartido de FACTURAS
# 1.2: Muestra los filtros en el template para ejecutar el API y cargar los resultados con Ajax desde el template
class FacturaFormView(GroupRequiredMixin, LoginRequiredMixin, FormView):
    group_required = [u"Operativo", u"Vendedor", u"Contador"]
    model = Factura
    form_class = FacturaRestForm
    template_name = 'transportes/factura_filter_list.html'




"""
    REPORTE EN PDF PARA FACTURA
"""

# Genera un recibo PDF
class FacturaTransporteView(View):
    def get(self, request, p_factura, *args, **kwargs):
        factura_base = Factura.objects.get(pk = p_factura)
        factura_detalle = Rutas.objects.filter(factura = p_factura)
        lv_fecha_hora = datetime.datetime.today().strftime('%Y-%m-%dT%H:%M:%S-06:00')
        data = {
			'ObjFactura': factura_base,
            'ObjDetalle': factura_detalle,
			'Dominio': settings.DOMINIO,
            'lv_fecha_hora': lv_fecha_hora,
		}
        pdf = render_to_pdf('reportes/imprimir_factura_transporte_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')



# Informe de ruta de vehículo
class InformeVelocidadRuta(View):
    def get(self, request, p_ruta, *args, **kwargs):
        objRuta = Rutas.objects.get(pk=p_ruta)
        objVehiculo = InventarioVehiculo.objects.get(pk=objRuta.vehiculo.id)
        new_end = objRuta.fecha_entrada_predio + datetime.timedelta(days=1) # a la última fecha hay que sumarle 1 día porque django ignora los datetime del último día para un rango: https://ajaxhispano.com/ask/django-database-query-como-filtrar-objetos-por-rango-de-fechas-4084/
        objLogVelocidadList = LogVelocidadesGPS.objects.filter(dispositivo_gps=objVehiculo.dispositivo_gps, creado__range = [objRuta.fecha_salida_predio, new_end])
        objLogVelocidades = LogVelocidadesGPS.objects.filter(dispositivo_gps=objVehiculo.dispositivo_gps, creado__range = [objRuta.fecha_salida_predio, new_end]).aggregate(Avg("velocidad_km"), Max("velocidad_km"), Min("velocidad_km"))
        velMin = objLogVelocidades['velocidad_km__min']
        velMax = objLogVelocidades['velocidad_km__max']
        velAvg = objLogVelocidades['velocidad_km__avg']

        velAlertada = LogVelocidadesGPS.objects.filter(dispositivo_gps=objVehiculo.dispositivo_gps, creado__range = [objRuta.fecha_salida_predio, new_end], velocidad_alertada=True).count()

        #import pdb; pdb.set_trace()

        data = {
			'objRuta': objRuta,
            'objVehiculo': objVehiculo,
            'objLogVelocidadList': objLogVelocidadList,
            'objLogVelocidades': objLogVelocidades,
			'Dominio': settings.DOMINIO,
            'velMin': velMin,
            'velMax': velMax,
            'velAvg': velAvg,
            'velAlertada': velAlertada,
		}
        pdf = render_to_pdf('reportes/imprimir_ruta_informe.html', data)
        return HttpResponse(pdf, content_type='application/pdf')