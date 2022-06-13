from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from django.views.generic import UpdateView, DetailView, ListView, CreateView, FormView, TemplateView, View
from django.urls import reverse_lazy, reverse

import datetime
from django.utils import timezone

# Decoradores para validar permisos de autenticación y grupos
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin

# Modelos
from apps.factura.models import Factura, Pedido, Ventas, EstadoPedido, Despacho
from apps.clientes.models import NegocioCliente
from django.contrib.auth.models import User
from apps.clientes.models import Cliente

# Formularios
from apps.factura.forms import PedidoAddAdminForm, PedidoUpdateAdminForm, \
FacturaCreateForm, FacturaUpdateForm, FacturaRestForm, VentasRestForm, VentasGlobalRestForm, \
DespachoForm, DespachoUpdateForm, PedidoPublicoRestForm, \
FacturaPublicoRestForm, DespachoPublicoRestForm


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
from .serializers import FacturaModelSerializer, VentasModelSerializer, PedidoModelSerializer, \
FacturaPublicoModelSerializer, DespachoPublicoModelSerializer
from .filters import FacturaFilterSet, VentasFilterSet, PedidoFilterSet, \
FacturaPublicoFilterSet, DespachoPublicoFilterSet




"""
    DESPACHO
"""
# Despacho | Agregar
class DespachoCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Supervisor", u"Operativo", u"Vendedor"]
    model = Despacho
    form_class = DespachoForm
    template_name = 'factura/despacho_add.html'

    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'negocio':lv_negocio, 'creado_por':self.request.user}

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(DespachoCreateView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs

    def get_success_url(self):
        return reverse('despacho_update', kwargs={'pk':self.object.id})
    

# Despacho | Actualizar
class DespachoUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Supervisor", u"Operativo", u"Vendedor"]
    model = Despacho
    form_class = DespachoUpdateForm
    template_name = 'factura/despacho_add.html'

    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'negocio':lv_negocio, 'actualizado_por':self.request.user}

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(DespachoUpdateView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs

    def get_success_url(self):
        return reverse('despacho_update', kwargs={'pk':self.object.id})




# 1.6 Lista los Despachos sin Completar
class DespachoListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Supervisor", u"Operativo", u"Vendedor"]
    model = Despacho
    paginate_by = 100
    template_name = 'factura/despacho_list.html'

    def get_queryset(self):
        queryset = super(DespachoListView, self).get_queryset()
        
        lv_negocio=None
        if self.request.user:
            lv_usuario = self.request.user
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        return queryset.filter(negocio=lv_negocio)
        

"""
    ./DESPACHO
"""



"""
    FACTURA
    ------------------ NO IMPLEMENTADO EN NINGÚN MODULO DE FORMA DIRECTA
"""
# Factura | Agregar
class FacturaCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Supervisor", u"Operativo", u"Vendedor", u"Contador"]
    model = Factura
    form_class = FacturaCreateForm
    template_name = 'factura/factura_add.html'


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
            return reverse('factura_update', kwargs={'pk':self.object.id}) # Sino tiene pedido, se redirecciona a la factura


# Factura | Actualizar
class FacturaAdminUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Supervisor", u"Operativo", u"Vendedor", u"Contador"]
    model = Factura
    form_class = FacturaUpdateForm
    template_name = 'factura/factura_update.html'

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(FacturaAdminUpdateView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs
    
    
    def get_success_url(self):
        return reverse('factura_update', kwargs={'pk':self.object.id})




"""
    PEDIDO
    ------------------
"""
# Pedido | Agregar | Páginas Administrativas
class PedidoAdminCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Supervisor", u"Operativo", u"Vendedor"]
    model = Pedido
    form_class = PedidoAddAdminForm
    template_name = 'factura/pedido_add.html'

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(PedidoAdminCreateView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs

    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'negocio':lv_negocio}

    # Validar formulario antes de guardar
    def form_valid(self, form):
        obj = form.save(commit=False)

        obj.fecha_pedido = datetime.datetime.now()

        # el negocio se pasa en el initial según el usuario logueado
        if obj.vendedor is None:
            obj.vendedor = self.request.user

        # Instancia de los tipos de pedido para obtener sólo el estado "Nueva Solicitud"
        ObjEstadoPedido = EstadoPedido.objects.get(id=1)
        obj.estado_pedido = ObjEstadoPedido

        return super(PedidoAdminCreateView, self).form_valid(form)

    
    def get_success_url(self):
        return reverse('pedido_update', kwargs={'pk':self.object.id})




# Pedido | Actualizar | Páginas Administrativas
class PedidoAdminUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Supervisor", u"Operativo", u"Vendedor", u"Contador"]
    model = Pedido
    form_class = PedidoUpdateAdminForm
    template_name = 'factura/pedido_update.html'


    def get_context_data(self, **kwargs):
        context = super(PedidoAdminUpdateView, self).get_context_data(**kwargs)
        
        if (self.object.relFacturaPedido.count() > 0):
            context['factura_orden'] = Factura.objects.get(pedido = self.object)
        

        lv_usuario = None
        if self.request.user:
            lv_usuario = self.request.user

        # Envía los valores iniciales al formulario en el detalle
        context['factura_orden_form'] = FacturaCreateForm(initial={'creado_por': lv_usuario,
                                                        'cliente':self.object.cliente,
                                                        'pedido':self.object,
                                                        'vendedor':self.object.vendedor,
                                                        'negocio':self.object.negocio,
                                                        'fecha_factura':datetime.datetime.now(),
                                                        'estado_factura':1,
                                                        })

        return context


    # Validar formulario antes de guardar
    def form_valid(self, form):
        obj = form.save(commit=False)

        # el negocio se pasa en el initial según el usuario logueado
        if obj.negocio and obj.vendedor is None:
            ObjVendedor = NegocioCliente.objects.get(negocio=obj.negocio)
            obj.vendedor = ObjVendedor.vendedor

        return super(PedidoAdminUpdateView, self).form_valid(form)


    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(PedidoAdminUpdateView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs
    
    def get_success_url(self):
        return reverse('pedido_update', kwargs={'pk':self.object.id})




# 1.6 Lista los Pedidos sin Completar
class PedidoListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Supervisor", u"Operativo", u"Vendedor", u"Contador"]
    model = Pedido
    paginate_by = 100
    template_name = 'factura/pedido_user_list.html'

    def get_queryset(self):
        queryset = super(PedidoListView, self).get_queryset()
        
        lv_usuario = None
        lv_negocio=None
        if self.request.user:
            lv_usuario = self.request.user
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        #relNegocioClienteVendedor__
        return queryset.filter(cliente__relNegocioClienteCliente__vendedor=lv_usuario, completado=False, negocio=lv_negocio).distinct()
        
    
    def get_context_data(self, **kwargs):
        context = super(PedidoListView, self).get_context_data(**kwargs)
        context['ahora'] = timezone.now()
        
        return context


# 1.6 Lista los Pedidos sin Completar General
class PedidoGeneralListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Supervisor", u"Operativo", u"Vendedor", u"Contador"]
    model = Pedido
    paginate_by = 100
    template_name = 'factura/pedido_general_list.html'

    def get_queryset(self):
        queryset = super(PedidoGeneralListView, self).get_queryset()
        
        lv_negocio=None
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        #relNegocioClienteVendedor__
        return queryset.filter(negocio=lv_negocio).distinct()
    
    def get_context_data(self, **kwargs):
        context = super(PedidoGeneralListView, self).get_context_data(**kwargs)
        context['ahora'] = timezone.now()
        
        return context

"""
    ./PEDIDO
    ------------------
"""





"""
INICIA: Filtros REST
====
"""

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




# 1.1: Representa el API, Utiliza el Serializer y el Filtro.
class FacturaListAPIView(ListAPIView):
    serializer_class = FacturaModelSerializer
    queryset = Factura.objects.all()
    filter_class = FacturaFilterSet
    pagination_class = ResultsSetPagination

# 1.2: Muestra los filtros en el template para ejecutar el API y cargar los resultados con Ajax desde el template
class FacturaFormView(GroupRequiredMixin, LoginRequiredMixin, FormView):
    group_required = [u"Administrativo", u"Supervisor", u"Operativo", u"Vendedor", u"Contador"]
    model = Factura
    form_class = FacturaRestForm
    template_name = 'factura/factura_filter_list.html'



# 2.1: Representa el API, Utiliza el Serializer y el Filtro.
class VentasListAPIView(ListAPIView):
    serializer_class = VentasModelSerializer
    queryset = Ventas.objects.all()
    filter_class = VentasFilterSet
    pagination_class = ResultsSetPagination

# 2.2: Muestra los filtros en el template para ejecutar el API y cargar los resultados con Ajax desde el template
class VentasFormView(GroupRequiredMixin, LoginRequiredMixin, FormView):
    group_required = [u"Administrativo", u"Supervisor", u"Operativo", u"Contador"]
    model = Ventas
    form_class = VentasRestForm
    template_name = 'factura/ventas_filter_list.html'



# 2.2: Muestra los filtros en el template para ejecutar el API y cargar los resultados con Ajax desde el template
class VentasGlobalFormView(GroupRequiredMixin, LoginRequiredMixin, FormView):
    group_required = [u"Administrativo"]
    model = Ventas
    form_class = VentasGlobalRestForm
    template_name = 'factura/ventas_filter_global_list.html'





"""
    ***********************************************
    API DE CLIENTES PUBLICO
    ***********************************************
"""

# 1.1: Representa el API, Utiliza el Serializer y el Filtro.
class PedidoListAPIView(ListAPIView):
    serializer_class = PedidoModelSerializer
    queryset = Pedido.objects.all()
    filter_class = PedidoFilterSet
    pagination_class = ResultsSetPagination

# 1.2: Muestra los filtros en el template para ejecutar el API y cargar los resultados con Ajax desde el template
class PedidoDetailView(DetailView):
    model = Cliente
    template_name = 'factura/cliente_pedido_filter_list.html'


    def get_context_data(self, **kwargs):
        context = super(PedidoDetailView, self).get_context_data(**kwargs)

        context['form'] = PedidoPublicoRestForm()
        
        return context


# 1.1: Representa el API, Utiliza el Serializer y el Filtro.
class FacturaPublicoListAPIView(ListAPIView):
    serializer_class = FacturaPublicoModelSerializer
    queryset = Factura.objects.all()
    filter_class = FacturaPublicoFilterSet
    pagination_class = ResultsSetPagination

# 1.2: Muestra los filtros en el template para ejecutar el API y cargar los resultados con Ajax desde el template
class FacturaPublicoDetailView(DetailView):
    model = Cliente
    template_name = 'factura/cliente_factura_filter_list.html'

    def get_context_data(self, **kwargs):
        context = super(FacturaPublicoDetailView, self).get_context_data(**kwargs)

        context['form'] = FacturaPublicoRestForm()
        
        return context




# 1.1: Representa el API, Utiliza el Serializer y el Filtro.
class DespachoPublicoListAPIView(ListAPIView):
    serializer_class = DespachoPublicoModelSerializer
    queryset = Despacho.objects.all()
    filter_class = DespachoPublicoFilterSet
    pagination_class = ResultsSetPagination

# 1.2: Muestra los filtros en el template para ejecutar el API y cargar los resultados con Ajax desde el template
class DespachoPublicoDetailView(DetailView):
    model = Cliente
    template_name = 'factura/cliente_despacho_filter_list.html'

    def get_context_data(self, **kwargs):
        context = super(DespachoPublicoDetailView, self).get_context_data(**kwargs)

        context['form'] = DespachoPublicoRestForm()
        
        return context


"""
    ***********************************************
    ./API DE CLIENTES PUBLICO
    ***********************************************
"""