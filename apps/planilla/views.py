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
from apps.planilla import models as m_planilla

# Formularios
from apps.planilla import forms as f_planilla




"""
    **************************************************
    Empleados
    **************************************************
"""
# 1.2. Agregar Empleados
class EmpleadosCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Contador", u"Operativo"]
    model = m_planilla.Empleados
    form_class = f_planilla.EmpleadosModelForm
    template_name = 'planilla/empleado_add.html'

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
        
        # el negocio se pasa en el initial según el usuario logueado
        if obj.creado_por is None:
            obj.creado_por = self.request.user

        return super(EmpleadosCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('empleado_list')


# 1.2. Actualizar Empleados
class EmpleadosUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Contador", u"Operativo"]
    model = m_planilla.Empleados
    form_class = f_planilla.EmpleadosModelForm
    template_name = 'planilla/empleado_add.html'

    def get_context_data(self, **kwargs):
        context = super(EmpleadosUpdateView, self).get_context_data(**kwargs)

        return context
    
    # Validar formulario antes de guardar
    def form_valid(self, form):
        obj = form.save(commit=False)

        # el negocio se pasa en el initial según el usuario logueado
        if obj.negocio is None:
            obj.negocio = self.request.user.relPerfilUsuario.negocio
        
        # el negocio se pasa en el initial según el usuario logueado
        if obj.actualizado_por is None:
            obj.actualizado_por = self.request.user
        
        return super(EmpleadosUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('empleado_list')


# 1.3. Lista de Empleados
class EmpleadosListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Contador", u"Operativo"]
    model = m_planilla.Empleados
    paginate_by = 100
    template_name = 'planilla/empleado_list.html'

    def get_queryset(self):
        queryset = super(EmpleadosListView, self).get_queryset()
        
        lv_negocio=None
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        return queryset.filter(negocio=lv_negocio)

"""
    **************************************************
    ./Empleados
    **************************************************
"""







"""
    **************************************************
    EncabezadoPlanilla
    **************************************************
"""
# 1.2. Agregar EncabezadoPlanilla
class EncabezadoPlanillaCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Contador", u"Operativo"]
    model = m_planilla.EncabezadoPlanilla
    form_class = f_planilla.EncabezadoPlanillaModelForm
    template_name = 'planilla/encabezado_add.html'

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
        
        # el negocio se pasa en el initial según el usuario logueado
        if obj.creado_por is None:
            obj.creado_por = self.request.user

        return super(EncabezadoPlanillaCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('encabezado_list')


# 1.2. Actualizar EncabezadoPlanilla
class EncabezadoPlanillaUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Contador", u"Operativo"]
    model = m_planilla.EncabezadoPlanilla
    form_class = f_planilla.EncabezadoPlanillaModelForm
    template_name = 'planilla/encabezado_add.html'

    def get_context_data(self, **kwargs):
        context = super(EncabezadoPlanillaUpdateView, self).get_context_data(**kwargs)

        p_negocio = self.request.user.relPerfilUsuario.negocio
        context['detalle_planilla_list'] = m_planilla.Planilla.objects.filter(encabezado_planilla = self.object, negocio=p_negocio)

        TotalSalarioBase = sum(registro.salario for registro in m_planilla.Planilla.objects.filter(encabezado_planilla = self.object))
        TotalBonificacionLey = sum(registro.bonificacion_de_ley for registro in m_planilla.Planilla.objects.filter(encabezado_planilla = self.object))
        TotalBonosExtras = sum(registro.bonos_extra for registro in m_planilla.Planilla.objects.filter(encabezado_planilla = self.object))
        TotalIGSS = sum(registro.igss for registro in m_planilla.Planilla.objects.filter(encabezado_planilla = self.object))

        context['total_planilla'] = TotalSalarioBase + TotalBonificacionLey + TotalBonosExtras + TotalIGSS

        return context
    
    # Validar formulario antes de guardar
    def form_valid(self, form):
        obj = form.save(commit=False)

        # el negocio se pasa en el initial según el usuario logueado
        if obj.negocio is None:
            obj.negocio = self.request.user.relPerfilUsuario.negocio
        
        # el negocio se pasa en el initial según el usuario logueado
        if obj.actualizado_por is None:
            obj.actualizado_por = self.request.user
        
        return super(EncabezadoPlanillaUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('encabezado_update', kwargs={'pk':self.object.id})


# 1.3. Lista de EncabezadoPlanilla
class EncabezadoPlanillaListView(GroupRequiredMixin, LoginRequiredMixin, ListView):
    group_required = [u"Contador", u"Operativo"]
    model = m_planilla.EncabezadoPlanilla
    paginate_by = 100
    template_name = 'planilla/encabezado_list.html'

    def get_queryset(self):
        queryset = super(EncabezadoPlanillaListView, self).get_queryset()
        
        lv_negocio=None
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        return queryset.filter(negocio=lv_negocio)

"""
    **************************************************
    ./EncabezadoPlanilla
    **************************************************
"""





"""
    **************************************************
    Planilla Mensual
    **************************************************
"""
# 1.2. Agregar Planilla
class PlanillaCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Contador", u"Operativo"]
    model = m_planilla.Planilla
    form_class = f_planilla.PlanillaModelForm
    template_name = 'planilla/planilla_add.html'

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
        
        # el negocio se pasa en el initial según el usuario logueado
        if obj.creado_por is None:
            obj.creado_por = self.request.user

        return super(PlanillaCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('encabezado_update', kwargs={'pk':self.object.encabezado_planilla.id})


# 1.2. Actualizar Planilla
class PlanillaUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Contador", u"Operativo"]
    model = m_planilla.Planilla
    form_class = f_planilla.PlanillaModelForm
    template_name = 'planilla/planilla_add.html'
    
    # Validar formulario antes de guardar
    def form_valid(self, form):
        obj = form.save(commit=False)

        # el negocio se pasa en el initial según el usuario logueado
        if obj.negocio is None:
            obj.negocio = self.request.user.relPerfilUsuario.negocio
        
        # el negocio se pasa en el initial según el usuario logueado
        if obj.actualizado_por is None:
            obj.actualizado_por = self.request.user
        
        return super(PlanillaUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('encabezado_update', kwargs={'pk':self.object.encabezado_planilla.id})


"""
    **************************************************
    ./Planilla Mensual
    **************************************************
"""