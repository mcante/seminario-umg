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
from apps.clientes.models import Cliente, NegocioCliente, Contacto
from apps.factura.models import Pedido, EstadoPedido

from apps.plantas.models import Inventario as PlantaInventario
from apps.transportes.models import InventarioVehiculo as TransporteInventario
from apps.ventas_y_alquileres.models import InventarioMaquinariaVentas as MaquinariaInventario
from apps.factura.models import Ventas
from apps.gastos.models import RegistroGastos


# Formularios
from apps.clientes.forms import ClienteForm, ClienteUpdateForm, ClienteRestForm, \
NegocioClienteForm, PedidoAddPublicForm, \
ClientePublicoForm, ContactoUpdateForm, ContactoPublicoForm



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
from .serializers import NegocioClienteModelSerializer, ClienteModelSerializer, \
ClientePublicModelSerializer, NegocioClientePublicModelSerializer
from .filters import NegocioClienteFilterSet, ClienteFilterSet, \
ClientePublicFilterSet, NegocioClientePublicFilterSet


"""
    HOME PAGE PUBLIC
"""

class InicioTemplateView(TemplateView):
    template_name = 'clientes/home_public/inicio.html'

class AcercaDeTemplateView(TemplateView):
    template_name = 'clientes/home_public/acerca.html'

class ContactoTemplateView(TemplateView):
    template_name = 'clientes/home_public/contact.html'

class PedidosSuccessTemplateView(TemplateView):
    template_name = 'clientes/home_public/pedidos_success.html'

class ContactoSuccessTemplateView(TemplateView):
    template_name = 'clientes/home_public/contacto_success.html'

class AccesoClientesTemplateView(TemplateView):
    template_name = 'clientes/home_public/clientes_access.html'

class PedidosTemplateView(TemplateView):
    template_name = 'clientes/home_public/pedidos.html'

    def get_context_data(self, **kwargs):
        context = super(PedidosTemplateView, self).get_context_data(**kwargs)

        #print(datetime.datetime.today().strftime('%Y-%m-%d'))

        ObjEstadoPedido = EstadoPedido.objects.get(id=1)
        
        # Agrega un formulario y lo pasa al contexto.
        context['pedido_cliente_form'] = PedidoAddPublicForm(initial={
                                                        'fecha_pedido':datetime.datetime.today().strftime('%Y-%m-%d'),
                                                        'estado_pedido':ObjEstadoPedido
                                                        })

        return context




# 1.1. Contacto | Agregar | Página Pública
class ContactoPublicCreateView(CreateView):
    model = Contacto
    form_class = ContactoPublicoForm
    template_name = 'clientes/home_public/contact.html'

    def get_success_url(self):
        return reverse('contacto_satisfactorio_view')


# 1.2. Actualizar Contacto
class ContactoUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Operativo", u"Vendedor"]
    model = Contacto
    form_class = ContactoUpdateForm
    template_name = 'clientes/contacto_update.html'

    def get_success_url(self):
        return reverse('contacto_update', kwargs={'pk':self.object.id})


# Lista los Contactos
class ContactoListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Vendedor", u"Operativo"]
    model = Contacto
    paginate_by = 100
    template_name = 'clientes/contacto_list.html'

    def get_queryset(self):
        queryset = super(ContactoListView, self).get_queryset()
        
        lv_negocio=None
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        return queryset.filter(negocio=lv_negocio)





# Pedido | Agregar | Página Pública
class PedidoPublicCreateView(CreateView):
    model = Pedido
    form_class = PedidoAddPublicForm
    template_name = 'clientes/home_public/pedidos_add.html'

    def get_success_url(self):
        return reverse('pedidos_satisfactorio_view')




class PerfilClienteDetailView(DetailView):
    model = Cliente
    form_class = ClientePublicoForm
    template_name = 'clientes/home_public/cliente_detail.html'

    def get_success_url(self):
        return reverse('acceso_clientes_view')




# PROMOCIÓN DE PRODUCTOS PUBLICOS

#PLANTA MINERA
class PlantaInventarioListView(ListView):
    model = PlantaInventario
    paginate_by = 100
    template_name = 'clientes/home_public/producto_minera.html'

    def get_queryset(self):
        queryset = super(PlantaInventarioListView, self).get_queryset()
        
        return queryset.filter(negocio__id=1)


#PLANTA TRANSFORMACIONES
class PlantaTransformacionesInventarioListView(ListView):
    model = PlantaInventario
    paginate_by = 100
    template_name = 'clientes/home_public/producto_transformaciones.html'

    def get_queryset(self):
        queryset = super(PlantaTransformacionesInventarioListView, self).get_queryset()
        
        return queryset.filter(negocio__id=2)

# TRANSPORTES
class TransporteInventarioListView(ListView):
    model = TransporteInventario
    paginate_by = 100
    template_name = 'clientes/home_public/producto_transportes.html'


# MAQUINARIA
class MaquinariaInventarioListView(ListView):
    model = MaquinariaInventario
    paginate_by = 100
    template_name = 'clientes/home_public/producto_maquinaria.html'



"""
    ./HOME PAGE PUBLIC
"""





# Dashboard
class PrincipalTemplateView(LoginRequiredMixin, TemplateView):
    #model = Cliente
    template_name = 'clientes/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super(PrincipalTemplateView, self).get_context_data(**kwargs)

        #VENTAS
        ObjVentasMinera = sum(registro.monto_venta for registro in Ventas.objects.filter(negocio__id=1))
        ObjVentasProcesados = sum(registro.monto_venta for registro in Ventas.objects.filter(negocio__id=2))
        ObjVentasConstructura = sum(registro.monto_venta for registro in Ventas.objects.filter(negocio__id=3))
        ObjVentasTransportes = sum(registro.monto_venta for registro in Ventas.objects.filter(negocio__id=4))
        ObjVentasMaquinas = sum(registro.monto_venta for registro in Ventas.objects.filter(negocio__id=5))

        context['venta_minera'] = int(ObjVentasMinera)
        context['venta_procesados'] = int(ObjVentasProcesados)
        context['venta_contructora'] = int(ObjVentasConstructura)
        context['venta_transportes'] = int(ObjVentasTransportes)
        context['venta_maquinas'] = int(ObjVentasMaquinas)


        #COMPRAS
        ObjGastosMinera = sum(registro.monto for registro in RegistroGastos.objects.filter(negocio__id=1))
        ObjGastosProcesados = sum(registro.monto for registro in RegistroGastos.objects.filter(negocio__id=2))
        ObjGastosConstructura = sum(registro.monto for registro in RegistroGastos.objects.filter(negocio__id=3))
        ObjGastosTransportes = sum(registro.monto for registro in RegistroGastos.objects.filter(negocio__id=4))
        ObjGastosMaquinas = sum(registro.monto for registro in RegistroGastos.objects.filter(negocio__id=5))

        context['gastos_minera'] = int(ObjGastosMinera)
        context['gastos_procesados'] = int(ObjGastosProcesados)
        context['gastos_contructora'] = int(ObjGastosConstructura)
        context['gastos_transportes'] = int(ObjGastosTransportes)
        context['gastos_maquinas'] = int(ObjGastosMaquinas)

        #import pdb; pdb.set_trace()

        return context







# Cliente | Agregar
class ClienteCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Operativo", u"Vendedor"]
    model = Cliente
    form_class = ClienteForm
    template_name = 'clientes/cliente_add.html'

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ClienteCreateView, self).get_form_kwargs()

        lv_negocio=None
        lv_tipo_empleado=None
        

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
            
        kwargs['p_negocio'] = lv_negocio
        
        return kwargs
    
    def get_success_url(self):
        return reverse('cliente_update', kwargs={'pk':self.object.id})



# 1.2. Actualizar Cliente
class ClienteUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Operativo", u"Vendedor"]
    model = Cliente
    form_class = ClienteUpdateForm
    template_name = 'clientes/cliente_update.html'

    def get_context_data(self, **kwargs):
        context = super(ClienteUpdateView, self).get_context_data(**kwargs)

        context['negocio_cliente_list'] = NegocioCliente.objects.filter(cliente=self.object)

        # Agrega un formulario y lo pasa al contexto.
        p_cliente = self.object
        context['negocio_cliente_form'] = NegocioClienteForm(p_cliente, initial={
                                                        'cliente':self.object,
                                                        'vendedor':self.request.user
                                                        })

        return context


    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ClienteUpdateView, self).get_form_kwargs()

        lv_negocio=None
        
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
            
        kwargs['p_negocio'] = lv_negocio
        
        return kwargs

    def get_success_url(self):
        return reverse('cliente_update', kwargs={'pk':self.object.id})



# NegocioCliente | Agregar
class NegocioClienteCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Operativo", u"Vendedor"]
    model = NegocioCliente
    form_class = NegocioClienteForm
    template_name = 'clientes/negocio_cliente_add.html'

    def get_success_url(self):
        return reverse('cliente_update', kwargs={'pk':self.object.cliente.id})






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
class ClienteListAPIView(ListAPIView):
    serializer_class = ClienteModelSerializer
    queryset = Cliente.objects.all()
    filter_class = ClienteFilterSet
    pagination_class = ResultsSetPagination

# 1.2: Muestra los filtros en el template para ejecutar el API y cargar los resultados con Ajax desde el template
class ClienteFormView(GroupRequiredMixin, LoginRequiredMixin, FormView):
    group_required = [u"Operativo", u"Vendedor"]
    #model = Cliente
    form_class = ClienteRestForm
    template_name = 'clientes/cliente_filter_list.html'


# 2.1: Representa el API, Utiliza el Serializer y el Filtro.
class NegocioClienteRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = NegocioClienteModelSerializer
    queryset = NegocioCliente.objects.all()
    filter_class = NegocioClienteFilterSet
    #pagination_class = ResultsSetPagination



# 3.1: Representa el API, Utiliza el Serializer y el Filtro.
class ClientePublicListAPIView(ListAPIView):
    serializer_class = ClientePublicModelSerializer
    queryset = Cliente.objects.all()
    filter_class = ClientePublicFilterSet

# 3.2: Representa el API, Utiliza el Serializer y el Filtro.
class NegocioClientePublicListAPIView(ListAPIView):
    serializer_class = NegocioClientePublicModelSerializer
    queryset = NegocioCliente.objects.all()
    filter_class = NegocioClientePublicFilterSet


"""
====
FINALIZA: ./Filtros REST
"""





class Error400TemplateView(TemplateView):
    template_name = 'error/404.html'


class Error505TemplateView(TemplateView):
    template_name = "home/404.html"

    @classmethod
    def as_error_view(cls):

        v = cls.as_view()
        def view(request):
            r = v(request)
            r.render()
            return r
        return view

