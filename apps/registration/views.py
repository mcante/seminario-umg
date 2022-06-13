from django.shortcuts import render
from django.db.models import Sum
import datetime

from apps.registration.models import NegocioUsuario, Presupuesto

from django.views.generic import UpdateView, DetailView, ListView, CreateView, FormView, TemplateView
from django.urls import reverse_lazy, reverse

# Decoradores para validar permisos de autenticación y grupos
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin

# Modelos
from apps.registration.models import Presupuesto
from apps.factura.models import Ventas
from apps.gastos.models import RegistroGastos

# Formularios
from apps.registration.forms import PresupuestoForm


# REST
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

# Serializadores y filtros para REST
from apps.registration.serializers import NegocioUsuarioModelSerializer
#from apps.registration.filters import 



"""
    ************************************
    PRESUPUESTO
    ************************************
"""


# Presupuesto | Agregar
class PresupuestoCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Administrativo", u"Supervisor", u"Contador", u"Operativo"]
    model = Presupuesto
    form_class = PresupuestoForm
    template_name = 'registration/presupuesto_add.html'

    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'negocio':lv_negocio, 'creado_por':self.request.user}

    # Validar formulario antes de guardar
    def form_valid(self, form):
        obj = form.save(commit=False)

        # el negocio se pasa en el initial según el usuario logueado
        if obj.negocio is None:
            obj.negocio = self.request.user.relPerfilUsuario.negocio
        
        if obj.creado_por is None:
            obj.creado_por = self.request.user

        return super(PresupuestoCreateView, self).form_valid(form)
    
    def get_success_url(self):
        return reverse('presupuesto_update', kwargs={'pk':self.object.id})



# 1.2. Actualizar Presupuesto
class PresupuestoUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Administrativo", u"Supervisor", u"Contador", u"Operativo"]
    model = Presupuesto
    form_class = PresupuestoForm
    template_name = 'registration/presupuesto_add.html'

    # Contexto
    def get_context_data(self, **kwargs):
        context = super(PresupuestoUpdateView, self).get_context_data(**kwargs)

        #context['documento_list'] = Documentos.objects.filter(proyecto=self.object)

        return context


    # Validar formulario antes de guardar
    def form_valid(self, form):
        obj = form.save(commit=False)

        # el negocio se pasa en el initial según el usuario logueado
        if obj.negocio is None:
            obj.negocio = self.request.user.relPerfilUsuario.negocio
        
        if obj.creado_por is None:
            obj.creado_por = self.request.user
        
        if obj.actualizado_por is None:
            obj.actualizado_por = self.request.user

        return super(PresupuestoUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('presupuesto_update', kwargs={'pk':self.object.id})


# 1.3 Lista los presupuestos 
class PresupuestoListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Administrativo", u"Supervisor", u"Contador", u"Operativo"]
    model = Presupuesto
    paginate_by = 100
    template_name = 'registration/presupuestos_list.html'

    def get_queryset(self):
        queryset = super(PresupuestoListView, self).get_queryset()
        return queryset.filter( negocio = self.request.user.relPerfilUsuario.negocio)


"""
    ************************************
    ./PRESUPUESTO
    ************************************
"""




class NegocioUsuarioTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'registration/switch_accesos_user.html'

    def get_context_data(self, **kwargs):
        context = super(NegocioUsuarioTemplateView, self).get_context_data(**kwargs)

        if self.request.user:
            lv_perfil_id = self.request.user.relPerfilUsuario.id

            context['object_list_access'] = NegocioUsuario.objects.filter(perfil_usuario=lv_perfil_id)

        return context





class FinancieroTemplateView(GroupRequiredMixin, LoginRequiredMixin, TemplateView):
    group_required = [u"Administrativo", u"Supervisor", u"Contador", u"Operativo"]
    template_name = 'registration/financiero_view.html'


    def get_context_data(self, **kwargs):
        context = super(FinancieroTemplateView, self).get_context_data(**kwargs)

        date = datetime.date.today()
        year = date.strftime("%Y")
        lv_negocio = None
        ObjVentas = None
        ObjRegistroGastos = None
        ObjPresupuesto = None
        ObjIngresos = None
        ObjBalanceGeneral = None
        try:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
            ObjVentas = sum(registro.monto_venta for registro in Ventas.objects.filter(negocio=lv_negocio))
            ObjRegistroGastos = sum(registro.monto for registro in RegistroGastos.objects.filter(negocio=lv_negocio))

            ObjPresupuesto = Presupuesto.objects.get(anio=year, negocio=lv_negocio)
            ObjIngresos = ((ObjPresupuesto.presupuesto_anual + ObjPresupuesto.excedente) + (ObjVentas))

            ObjBalanceGeneral = '{:,.2f}'.format(ObjIngresos - ObjRegistroGastos)

            # Reformatear
            ObjVentas = '{:,.2f}'.format(ObjVentas)
            ObjRegistroGastos = '{:,.2f}'.format(ObjRegistroGastos)
            #ObjPresupuesto = ObjPresupuesto
            ObjIngresos = '{:,.2f}'.format(ObjIngresos)
        except:
            pass
        

        print(ObjIngresos)
        
        # Ingresos
        context['ObjPresupuesto'] = ObjPresupuesto
        context['ObjVentas'] = ObjVentas
        context['ObjIngresos'] = ObjIngresos
        # Egresos
        context['ObjGastos'] = ObjRegistroGastos
        # Balance General
        context['ObjBalanceGeneral'] = ObjBalanceGeneral
        

        
        
        return context





"""
INICIA: REST
====
"""

# 1.1: Representa el API, Utiliza el Serializer y el Filtro.
class NegocioUsuarioRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = NegocioUsuarioModelSerializer
    queryset = NegocioUsuario.objects.all()


"""
====
FINALIZA: ./ REST
"""