from django.shortcuts import render
from django.http import JsonResponse, HttpResponse

from django.views.generic import UpdateView, DetailView, ListView, CreateView, FormView, TemplateView, View
from django.urls import reverse_lazy, reverse

import datetime
from django.utils import timezone

# Configuración del settings, variables
from django.conf import settings

# Decoradores para validar permisos de autenticación y grupos
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin

# Modelos
from .models import Medidas, Producto, DetalleFactura, Inventario, IngresoCompras
from apps.proveedores.models import Proveedor
from apps.factura.models import Factura

# Formularios
from apps.plantas.forms import ProveedorForm, ProveedorUpdateForm, \
MedidasForm, MedidasUpdateForm, \
ProductoForm, ProductoUpdateForm, \
InventarioRestForm, InventarioForm, InventarioUpdateForm, DetalleFacturaForm, \
IngresoComprasCreateForm, \
FacturaCreateForm, FacturaUpdateForm

# Formulario compartido de FACTURAS
from apps.factura.forms import FacturaRestForm


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
from .serializers import InventarioModelSerializer, DetalleFacturaModelSerializer
from .filters import InventarioFilterSet, DetalleFacturaFilterSet


# Render personalizado para pdf
from apps.factura.htmltopdf import render_to_pdf


# Proveedor | Agregar
class ProveedorCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Supervisor", u"Operativo"]
    model = Proveedor
    form_class = ProveedorForm
    template_name = 'plantas/proveedor_add.html'

    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'negocio':lv_negocio}


    def get_success_url(self):
        return reverse('proveedor_update', kwargs={'pk':self.object.id})



# 1.2. Actualizar Proveedor
class ProveedorUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Supervisor", u"Operativo"]
    model = Proveedor
    form_class = ProveedorUpdateForm
    template_name = 'plantas/proveedor_add.html'


    # Validar formulario antes de guardar
    def form_valid(self, form):
        obj = form.save(commit=False)

        # el negocio se pasa en el initial según el usuario logueado
        if obj.negocio is None:
            obj.negocio = self.request.user.relPerfilUsuario.negocio

        return super(ProveedorUpdateView, self).form_valid(form)


    def get_success_url(self):
        return reverse('proveedor_update', kwargs={'pk':self.object.id})




# Lista los Proveedores
class ProveedorListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Supervisor", u"Operativo"]
    model = Proveedor
    paginate_by = 100
    template_name = 'plantas/proveedores_list.html'

    def get_queryset(self):
        queryset = super(ProveedorListView, self).get_queryset()
        
        lv_negocio=None
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        return queryset.filter(negocio=lv_negocio)





# Medida | Agregar
class MedidasCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Supervisor", u"Operativo"]
    model = Medidas
    form_class = MedidasForm
    template_name = 'plantas/medida_add.html'

    def get_success_url(self):
        return reverse('medida_update', kwargs={'pk':self.object.id})


# 1.2. Actualizar Medida
class MedidasUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Supervisor", u"Operativo"]
    model = Medidas
    form_class = MedidasUpdateForm
    template_name = 'plantas/medida_add.html'


    def get_success_url(self):
        return reverse('medida_update', kwargs={'pk':self.object.id})


# 1.3. Lista los Medidas
class MedidasListView(ListView):
    group_required = [u"Supervisor", u"Operativo"]
    model = Medidas
    paginate_by = 100
    template_name = 'plantas/medidas_list.html'







# Producto | Agregar
class ProductoCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Supervisor", u"Operativo"]
    model = Producto
    form_class = ProductoForm
    template_name = 'plantas/producto_add.html'

    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'negocio':lv_negocio, 'creado_por':self.request.user}
    
    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ProductoCreateView, self).get_form_kwargs()

        lv_negocio=None
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs

    def get_success_url(self):
        return reverse('producto_update', kwargs={'pk':self.object.id})


# 1.2. Actualizar Producto
class ProductoUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Supervisor", u"Operativo"]
    model = Producto
    form_class = ProductoUpdateForm
    template_name = 'plantas/producto_add.html'

    # Validar formulario antes de guardar
    def form_valid(self, form):
        obj = form.save(commit=False)

        # el negocio se pasa en el initial según el usuario logueado
        if obj.negocio is None:
            obj.negocio = self.request.user.relPerfilUsuario.negocio
        
        if obj.actualizado_por is None:
            obj.actualizado_por = self.request.user

        return super(ProductoUpdateView, self).form_valid(form)


    def get_success_url(self):
        return reverse('producto_update', kwargs={'pk':self.object.id})


# 1.3. Lista los Producto
class ProductoListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Supervisor", u"Operativo", u"Vendedor"]
    model = Producto
    paginate_by = 100
    template_name = 'plantas/productos_list.html'

    def get_queryset(self):
        queryset = super(ProductoListView, self).get_queryset()
        
        lv_negocio=None
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        return queryset.filter(negocio=lv_negocio)








# Inventario | Agregar
class InventarioCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Supervisor", u"Operativo"]
    model = Inventario
    form_class = InventarioForm
    template_name = 'plantas/inventario_add.html'

    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'negocio':lv_negocio, 'creado_por':self.request.user}
    
    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(InventarioCreateView, self).get_form_kwargs()

        lv_negocio=None
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs

    def get_success_url(self):
        return reverse('inventario_update', kwargs={'pk':self.object.id})


# 1.2. Actualizar Inventario
class InventarioUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Supervisor", u"Operativo"]
    model = Inventario
    form_class = InventarioUpdateForm
    template_name = 'plantas/inventario_add.html'


    # Validar formulario antes de guardar
    def form_valid(self, form):
        obj = form.save(commit=False)

        # el negocio se pasa en el initial según el usuario logueado
        if obj.negocio is None:
            obj.negocio = self.request.user.relPerfilUsuario.negocio
        
        if obj.actualizado_por is None:
            obj.actualizado_por = self.request.user

        return super(InventarioUpdateView, self).form_valid(form)


    def get_success_url(self):
        return reverse('inventario_update', kwargs={'pk':self.object.id})





""" IngresoCompras """


# IngresoCompras | Agregar
class IngresoComprasCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Contador", u"Operativo"]
    model = IngresoCompras
    form_class = IngresoComprasCreateForm
    template_name = 'plantas/ingreso_inventario_compras_add.html'

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
        return reverse('plantas_ingreso_inventario_compras_update', kwargs={'pk':self.object.id})



    
# IngresoCompras | Actualizar
class IngresoComprasUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Contador", u"Operativo"]
    model = IngresoCompras
    form_class = IngresoComprasCreateForm
    template_name = 'plantas/ingreso_inventario_compras_add.html'

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
        return reverse('plantas_ingreso_inventario_compras_update', kwargs={'pk':self.object.id})



# Lista los IngresoCompras
class IngresoComprasListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Administrativo", u"Supervisor", u"Operativo"]
    model = IngresoCompras
    paginate_by = 100
    template_name = 'plantas/ingreso_inventario_compras_list.html'

    def get_queryset(self):
        queryset = super(IngresoComprasListView, self).get_queryset()
        
        lv_negocio=None
        if self.request.user:
            lv_usuario = self.request.user
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        #relNegocioClienteVendedor__
        return queryset.filter(negocio=lv_negocio).distinct()



""" ./ IngresoCompras """








"""
    FACTURA
    ------------------
"""
# Factura | Agregar
class FacturaCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Operativo", u"Vendedor", u"Contador"]
    model = Factura
    form_class = FacturaCreateForm
    template_name = 'plantas/factura_add.html'


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
            return reverse('planta_factura_update', kwargs={'pk':self.object.id}) # Sino tiene pedido, se redirecciona a la factura






# Factura | Actualizar
class FacturaUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Operativo", u"Vendedor", u"Contador"]
    model = Factura
    form_class = FacturaUpdateForm
    template_name = 'plantas/factura_update.html'

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
        return reverse('planta_factura_update', kwargs={'pk':self.object.id})







# DetalleFactura | Agregar
class DetalleFacturaCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Operativo", u"Vendedor", u"Contador"]
    model = DetalleFactura
    form_class = DetalleFacturaForm
    template_name = 'plantas/detalle_factura_add.html'


    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(DetalleFacturaCreateView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs

    def get_success_url(self):
        return reverse('planta_factura_update', kwargs={'pk':self.object.factura.id})






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
class InventarioListAPIView(ListAPIView):
    serializer_class = InventarioModelSerializer
    queryset = Inventario.objects.all()
    filter_class = InventarioFilterSet
    pagination_class = ResultsSetPagination

# 1.2: Muestra los filtros en el template para ejecutar el API y cargar los resultados con Ajax desde el template
class InventarioFormView(GroupRequiredMixin, LoginRequiredMixin, FormView):
    group_required = [u"Administrativo", u"Supervisor", u"Operativo", u"Vendedor"]
    model = Inventario
    form_class = InventarioRestForm
    template_name = 'plantas/inventario_filter_list.html'
    

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(InventarioFormView, self).get_form_kwargs()

        lv_negocio=None
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs



class FacturaFormView(GroupRequiredMixin, LoginRequiredMixin, FormView):
    group_required = [u"Administrativo", u"Supervisor", u"Operativo", u"Vendedor", u"Contador"]
    model = Factura
    form_class = FacturaRestForm
    template_name = 'plantas/factura_filter_list.html'


# Para quitar productos del detalle
# 2.1: Representa el API, Utiliza el Serializer y el Filtro.
class DetalleFacturaRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = DetalleFacturaModelSerializer
    queryset = DetalleFactura.objects.all()
    filter_class = DetalleFacturaFilterSet



"""
    REPORTE EN PDF PARA FACTURA
"""

# Genera un recibo PDF
class FacturaPlantaView(View):
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
        pdf = render_to_pdf('reportes/imprimir_factura_planta_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
