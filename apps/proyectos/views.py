# DEPURADOR
# import pdb; pdb.set_trace()

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
from .models import TipoProyecto, Proyecto, Documentos, GastosProyecto, DetalleFacturaEntregables
from apps.proveedores.models import Proveedor
from apps.factura.models import Factura

# Formularios
from .forms import ProyectoForm, ProyectoUpdateForm, DocumentosForm, GastosProyectoForm, \
FacturaCreateForm, FacturaUpdateForm, DetalleFacturaEntregablesForm

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
#from .serializers import InventarioModelSerializer, DetalleFacturaModelSerializer
#from .filters import InventarioFilterSet, DetalleFacturaFilterSet



# Render personalizado para pdf
from apps.factura.htmltopdf import render_to_pdf


# Proyecto | Agregar
class ProyectoCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Supervisor", u"Operativo", u"Vendedor"]
    model = Proyecto
    form_class = ProyectoForm
    template_name = 'proyectos/proyecto_add.html'

    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'negocio':lv_negocio, 'creado_por':self.request.user}
    

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(ProyectoCreateView, self).get_form_kwargs()

        lv_negocio=None
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs


    def get_success_url(self):
        return reverse('proyecto_update', kwargs={'pk':self.object.id})



# 1.2. Actualizar Proyecto
class ProyectoUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Supervisor", u"Operativo", u"Vendedor"]
    model = Proyecto
    form_class = ProyectoUpdateForm
    template_name = 'proyectos/proyecto_update.html'

    # Contexto
    def get_context_data(self, **kwargs):
        context = super(ProyectoUpdateView, self).get_context_data(**kwargs)

        context['documento_list'] = Documentos.objects.filter(proyecto=self.object)

        # Agrega el formulario para agregar documentos contexto
        context['documento_form'] = DocumentosForm(initial={
                                                        'proyecto':self.object,
                                                        'negocio':self.request.user.relPerfilUsuario.negocio,
                                                        'creado_por':self.request.user
                                                        })
        
        context['gastos_list'] = GastosProyecto.objects.filter(proyecto=self.object)

        # Agrega el formulario para agregar documentos contexto
        context['gastos_proyecto_form'] = GastosProyectoForm(initial={
                                                        'proyecto':self.object,
                                                        'negocio':self.request.user.relPerfilUsuario.negocio,
                                                        'creado_por':self.request.user
                                                        })

        context['entregables_proyecto_list'] = DetalleFacturaEntregables.objects.filter(proyecto=self.object)

        return context


    # Validar formulario antes de guardar
    def form_valid(self, form):
        obj = form.save(commit=False)

        # el negocio se pasa en el initial según el usuario logueado
        if obj.negocio is None:
            obj.negocio = self.request.user.relPerfilUsuario.negocio

        return super(ProyectoUpdateView, self).form_valid(form)


    def get_success_url(self):
        return reverse('proyecto_update', kwargs={'pk':self.object.id})




# 1.3. Lista de Proyectos
class ProyectoListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Administrador", u"Supervisor", u"Operativo", u"Vendedor"]
    model = Proyecto
    paginate_by = 100
    template_name = 'proyectos/proyecto_list.html'

    def get_queryset(self):
        queryset = super(ProyectoListView, self).get_queryset()
        
        lv_negocio=None
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        return queryset.filter(negocio=lv_negocio)





# Documentos | Agregar
class DocumentosCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Operativo", u"Supervisor", u"Vendedor"]
    model = Documentos
    form_class = DocumentosForm
    template_name = 'proyectos/documento_add.html'

    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'negocio':lv_negocio, 'creado_por':self.request.user}


    def get_success_url(self):
        return reverse('proyecto_update', kwargs={'pk':self.object.proyecto.id})




# GastosProyecto | Agregar
class GastosProyectoCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Operativo", u"Supervisor", u"Vendedor", u"Contador"]
    model = GastosProyecto
    form_class = GastosProyectoForm
    template_name = 'proyectos/gastos_proyecto_add.html'

    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'negocio':lv_negocio, 'creado_por':self.request.user}


    def get_success_url(self):
        return reverse('proyecto_update', kwargs={'pk':self.object.proyecto.id})









"""
    FACTURA
    ------------------
"""
# Factura | Agregar
class FacturaCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Operativo", u"Vendedor", u"Contador"]
    model = Factura
    form_class = FacturaCreateForm
    template_name = 'proyectos/factura_add.html'


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
            return reverse('proyectos_factura_update', kwargs={'pk':self.object.id}) # Sino tiene pedido, se redirecciona a la factura





# Factura | Actualizar
class FacturaUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Operativo", u"Vendedor", u"Contador"]
    model = Factura
    form_class = FacturaUpdateForm
    template_name = 'proyectos/factura_update.html'

    def get_context_data(self, **kwargs):
        context = super(FacturaUpdateView, self).get_context_data(**kwargs)
        
        context['detalle_factura_list'] = DetalleFacturaEntregables.objects.filter(factura = self.object)

        # Agrega un formulario y lo pasa al contexto.
        p_negocio = self.request.user.relPerfilUsuario.negocio
        context['detalle_factura_form'] = DetalleFacturaEntregablesForm(p_negocio, initial={
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
        return reverse('proyectos_factura_update', kwargs={'pk':self.object.id})







# DetalleFacturaEntregables | Agregar
class DetalleFacturaEntregablesCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Contador", u"Operativo", u"Vendedor"]
    model = DetalleFacturaEntregables
    form_class = DetalleFacturaEntregablesForm
    template_name = 'proyectos/detalle_factura_add.html'


    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(DetalleFacturaEntregablesCreateView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs

    def get_success_url(self):
        return reverse('proyectos_factura_update', kwargs={'pk':self.object.factura.id})






# Formulario compartido de FACTURAS
# 1.2: Muestra los filtros en el template para ejecutar el API y cargar los resultados con Ajax desde el template
class FacturaFormView(GroupRequiredMixin, LoginRequiredMixin, FormView):
    group_required = [u"Operativo", u"Vendedor", u"Contador"]
    model = Factura
    form_class = FacturaRestForm
    template_name = 'proyectos/factura_filter_list.html'





"""
    REPORTE EN PDF PARA FACTURA
"""

# Genera un recibo PDF
class FacturaConstructoraView(View):
    def get(self, request, p_factura, *args, **kwargs):
        factura_base = Factura.objects.get(pk = p_factura)
        factura_detalle = DetalleFacturaEntregables.objects.filter(factura = p_factura)
        lv_fecha_hora = datetime.datetime.today().strftime('%Y-%m-%dT%H:%M:%S-06:00')
        data = {
			'ObjFactura': factura_base,
            'ObjDetalle': factura_detalle,
			'Dominio': settings.DOMINIO,
            'lv_fecha_hora': lv_fecha_hora,
		}
        pdf = render_to_pdf('reportes/imprimir_factura_constructora_pdf.html', data)
        return HttpResponse(pdf, content_type='application/pdf')
