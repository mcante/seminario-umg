from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from django.views.generic import UpdateView, DetailView, ListView, CreateView, FormView, TemplateView, View
from django.urls import reverse_lazy, reverse

import datetime
from django.utils import timezone

# Decoradores para validar permisos de autenticación y grupos
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin

# Configuración del settings, variables
from django.conf import settings

# Modelos
from django.contrib.auth.models import User

from .models import Marca, TipoMaquina, Maquina, InventarioMaquinariaVentas, \
IngresoCompras, InventarioMaquinariaAlquiler, EstadoAlquiler, AlquilerMaquina, DetalleFactura

from apps.factura.models import Factura

# Formulario compartido de FACTURAS
from apps.factura.forms import FacturaRestForm

# Formularios
from .forms import MaquinaCreateForm, InventarioMaquinariaVentasCreateForm, IngresoComprasCreateForm, \
InventarioMaquinariaAlquilerCreateForm, AlquilerMaquinaCreateForm, \
FacturaCreateForm, FacturaUpdateForm, DetalleFacturaForm


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
from .serializers import InventarioMaquinariaVentasModelSerializer, DetalleFacturaModelSerializer, \
InventarioMaquinariaAlquilerModelSerializer, AlquilerMaquinaModelSerializer
from .filters import InventarioMaquinariaVentasFilterSet, DetalleFacturaFilterSet, \
InventarioMaquinariaAlquilerFilterSet, AlquilerMaquinaFilterSet


# Render personalizado para pdf
from apps.factura.htmltopdf import render_to_pdf



""" Maquina """

# Maquina | Agregar
class MaquinaCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Contador", u"Operativo"]
    model = Maquina
    form_class = MaquinaCreateForm
    template_name = 'ventas_y_alquileres/maquina_add.html'

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(MaquinaCreateView, self).get_form_kwargs()

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
        return reverse('maquina_update', kwargs={'pk':self.object.id})

    
# Maquina | Actualizar
class MaquinaUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Contador", u"Operativo"]
    model = Maquina
    form_class = MaquinaCreateForm
    template_name = 'ventas_y_alquileres/maquina_add.html'

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(MaquinaUpdateView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs

    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'actualizado_por':self.request.user}

    def get_success_url(self):
        return reverse('maquina_update', kwargs={'pk':self.object.id})



# Lista los Maquina
class MaquinaListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Contador", u"Supervisor", u"Operativo", u"Vendedor"]
    model = Maquina
    paginate_by = 100
    template_name = 'ventas_y_alquileres/maquina_list.html'



""" ./ Maquina """









""" InventarioMaquinariaVentas """


# InventarioMaquinariaVentas | Agregar
class InventarioMaquinariaVentasCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Administrativo", u"Contador", u"Operativo"]
    model = InventarioMaquinariaVentas
    form_class = InventarioMaquinariaVentasCreateForm
    template_name = 'ventas_y_alquileres/inventario_maquina_ventas_add.html'

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(InventarioMaquinariaVentasCreateView, self).get_form_kwargs()

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
        return reverse('inventario_ventas_update', kwargs={'pk':self.object.id})

    
# InventarioMaquinariaVentas | Actualizar
class InventarioMaquinariaVentasUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Contador", u"Supervisor", u"Operativo"]
    model = InventarioMaquinariaVentas
    form_class = InventarioMaquinariaVentasCreateForm
    template_name = 'ventas_y_alquileres/inventario_maquina_ventas_add.html'

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(InventarioMaquinariaVentasUpdateView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs

    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'actualizado_por':self.request.user}

    def get_success_url(self):
        return reverse('inventario_ventas_update', kwargs={'pk':self.object.id})



# Lista los InventarioMaquinariaVentas
class InventarioMaquinariaVentasListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Contador", u"Supervisor", u"Operativo", u"Vendedor"]
    model = InventarioMaquinariaVentas
    paginate_by = 100
    template_name = 'ventas_y_alquileres/inventario_maquina_ventas_list.html'



""" ./ InventarioMaquinariaVentas """









""" IngresoCompras """


# IngresoCompras | Agregar
class IngresoComprasCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Contador", u"Operativo"]
    model = IngresoCompras
    form_class = IngresoComprasCreateForm
    template_name = 'ventas_y_alquileres/ingreso_inventario_compras_add.html'

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(IngresoComprasCreateView, self).get_form_kwargs()

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
        return reverse('ingreso_inventario_compras_update', kwargs={'pk':self.object.id})

    
# IngresoCompras | Actualizar
class IngresoComprasUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Contador", u"Operativo"]
    model = IngresoCompras
    form_class = IngresoComprasCreateForm
    template_name = 'ventas_y_alquileres/ingreso_inventario_compras_add.html'

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(IngresoComprasUpdateView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs

    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'actualizado_por':self.request.user}

    def get_success_url(self):
        return reverse('ingreso_inventario_compras_update', kwargs={'pk':self.object.id})



# Lista los IngresoCompras
class IngresoComprasListView(ListView):
    group_required = [u"Contador", u"Supervisor", u"Operativo"]
    model = IngresoCompras
    paginate_by = 100
    template_name = 'ventas_y_alquileres/ingreso_inventario_compras_list.html'



""" ./ IngresoCompras """




""" InventarioMaquinariaAlquiler """


# InventarioMaquinariaAlquiler | Agregar
class InventarioMaquinariaAlquilerCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Contador", u"Supervisor", u"Operativo"]
    model = InventarioMaquinariaAlquiler
    form_class = InventarioMaquinariaAlquilerCreateForm
    template_name = 'ventas_y_alquileres/inventario_alquiler_add.html'

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(InventarioMaquinariaAlquilerCreateView, self).get_form_kwargs()

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
        return reverse('inventario_alquiler_update', kwargs={'pk':self.object.id})

    
# InventarioMaquinariaAlquiler | Actualizar
class InventarioMaquinariaAlquilerUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Contador", u"Operativo"]
    model = InventarioMaquinariaAlquiler
    form_class = InventarioMaquinariaAlquilerCreateForm
    template_name = 'ventas_y_alquileres/inventario_alquiler_add.html'

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(InventarioMaquinariaAlquilerUpdateView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs

    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'actualizado_por':self.request.user}

    def get_success_url(self):
        return reverse('inventario_alquiler_update', kwargs={'pk':self.object.id})



# Lista los InventarioMaquinariaAlquiler
class InventarioMaquinariaAlquilerListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Contador", u"Supervisor", u"Operativo", u"Vendedor"]
    model = InventarioMaquinariaAlquiler
    paginate_by = 100
    template_name = 'ventas_y_alquileres/inventario_alquiler_list.html'



""" ./ IngresoCompras """






""" AlquilerMaquina """


# AlquilerMaquina | Agregar
class AlquilerMaquinaCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Operativo", u"Vendedor"]
    model = AlquilerMaquina
    form_class = AlquilerMaquinaCreateForm
    template_name = 'ventas_y_alquileres/alquiler_maquina_add.html'

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AlquilerMaquinaCreateView, self).get_form_kwargs()

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
        return reverse('alquiler_maquina_update', kwargs={'pk':self.object.id})

    
# AlquilerMaquina | Actualizar
class AlquilerMaquinaUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Operativo", u"Vendedor"]
    model = AlquilerMaquina
    form_class = AlquilerMaquinaCreateForm
    template_name = 'ventas_y_alquileres/alquiler_maquina_add.html'

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(AlquilerMaquinaUpdateView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs

    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'actualizado_por':self.request.user}

    def get_success_url(self):
        return reverse('alquiler_maquina_update', kwargs={'pk':self.object.id})



# Lista los AlquilerMaquina
class AlquilerMaquinaListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Contador", u"Operativo", u"Vendedor"]
    model = AlquilerMaquina
    paginate_by = 100
    template_name = 'ventas_y_alquileres/alquiler_maquina_list.html'



""" ./ IngresoCompras """






"""
    FACTURA
    ------------------
"""
# Factura | Agregar
class FacturaCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Operativo", u"Vendedor"]
    model = Factura
    form_class = FacturaCreateForm
    template_name = 'ventas_y_alquileres/factura_add.html'


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
            return reverse('maquinas_factura_update', kwargs={'pk':self.object.id}) # Sino tiene pedido, se redirecciona a la factura






# Factura | Actualizar
class FacturaUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Operativo", u"Vendedor"]
    model = Factura
    form_class = FacturaUpdateForm
    template_name = 'ventas_y_alquileres/factura_update.html'

    def get_context_data(self, **kwargs):
        context = super(FacturaUpdateView, self).get_context_data(**kwargs)
        
        context['detalle_factura_list'] = DetalleFactura.objects.filter(factura = self.object)
        

        # Agrega un formulario y lo pasa al contexto.
        p_negocio = self.request.user.relPerfilUsuario.negocio
        context['detalle_factura_form'] = DetalleFacturaForm(p_negocio, initial={
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
        return reverse('maquinas_factura_update', kwargs={'pk':self.object.id})




# DetalleFactura | Agregar
class DetalleFacturaCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Operativo", u"Vendedor"]
    model = DetalleFactura
    form_class = DetalleFacturaForm
    template_name = 'ventas_y_alquileres/detalle_factura_add.html'


    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(DetalleFacturaCreateView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs

    def get_success_url(self):
        return reverse('maquinas_factura_update', kwargs={'pk':self.object.factura.id})






"""
INICIA: Filtros REST
====
"""


# Formulario compartido de FACTURAS
# 1.1: Muestra los filtros en el template para ejecutar el API y cargar los resultados con Ajax desde el template
class FacturaFormView(GroupRequiredMixin, LoginRequiredMixin, FormView):
    group_required = [u"Supervisor", u"Operativo", u"Vendedor"]
    model = Factura
    form_class = FacturaRestForm
    template_name = 'ventas_y_alquileres/factura_filter_list.html'





class ResultsSetPagination(PageNumberPagination):
    page_size = 100
    page_size_query_param = 'page_size'
    max_page_size = 1000

    
    def get_paginated_response(self, data):

        # Recuperamos los valores por defecto
        next_link = self.get_next_link()
        previous_link = self.get_previous_link()

        # Hacemos un split en la primera '/' dejando sólo los parámetros
        """
        if next_link:
            next_link = next_link.split('http://127.0.0.1:8000')[1]

        if previous_link:
            previous_link = previous_link.split('http://127.0.0.1:8000')[1]
        """

        return Response({
            
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'total_pages': self.page.paginator.num_pages,
            'count': self.page.paginator.count,
            'anterior': previous_link,
            'siguiente': next_link,
            'results': data
        })


# 2.1: Representa el API, Utiliza el Serializer y el Filtro. (VENTAS)
class InventarioMaquinariaVentasListAPIView(ListAPIView):
    serializer_class = InventarioMaquinariaVentasModelSerializer
    queryset = InventarioMaquinariaVentas.objects.all()
    filter_class = InventarioMaquinariaVentasFilterSet
    pagination_class = ResultsSetPagination

# 2.2: Representa el API, Utiliza el Serializer y el Filtro. (ALQUILER)
class InventarioMaquinariaAlquilerListAPIView(ListAPIView):
    serializer_class = InventarioMaquinariaAlquilerModelSerializer
    queryset = InventarioMaquinariaAlquiler.objects.all()
    filter_class = InventarioMaquinariaAlquilerFilterSet
    pagination_class = ResultsSetPagination


# 2.3: Representa el API, Utiliza el Serializer y el Filtro. (ficha ALQUILER)
class AlquilerMaquinaListAPIView(ListAPIView):
    serializer_class = AlquilerMaquinaModelSerializer
    queryset = AlquilerMaquina.objects.all()
    filter_class = AlquilerMaquinaFilterSet
    pagination_class = ResultsSetPagination



# Para quitar productos del detalle
# 3.1: Representa el API, Utiliza el Serializer y el Filtro.
class DetalleFacturaRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DetalleFacturaModelSerializer
    queryset = DetalleFactura.objects.all()
    filter_class = DetalleFacturaFilterSet




"""
    REPORTE EN PDF PARA FACTURA
"""

# Genera un recibo PDF
class FacturaMaquinariaView(View):
    def get(self, request, p_factura, *args, **kwargs):
        factura_base = Factura.objects.get(pk = p_factura)
        factura_detalle = DetalleFactura.objects.filter(factura = p_factura)
        lv_fecha_hora = datetime.datetime.today().strftime('%Y-%m-%dT%H:%M:%S-06:00')
        data = {
			'ObjFactura': factura_base,
            'ObjDetalle': factura_detalle,
			'Dominio': settings.DOMINIO,
            'lv_fecha_hora': lv_fecha_hora,
		}
        pdf = render_to_pdf('reportes/imprimir_factura_maquinaria_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
