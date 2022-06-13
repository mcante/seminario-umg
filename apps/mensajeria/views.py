from django.db.models import Q

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
from apps.mensajeria import models as m_mensajeria

# Formularios
from apps.mensajeria import forms as f_mensajeria




"""
    **************************************************
    Encabezado de Mensajes
    **************************************************
"""
# 1.2. Agregar EncabezadoMensaje
class EncabezadoMensajeCreateView(LoginRequiredMixin, CreateView):
    model = m_mensajeria.EncabezadoMensaje
    form_class = f_mensajeria.EncabezadoMensajeModelForm
    template_name = 'mensajeria/encabezado_mensaje_add.html'

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(EncabezadoMensajeCreateView, self).get_form_kwargs()

        lv_negocio=None
        
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
            
        kwargs['p_negocio'] = lv_negocio
        
        return kwargs

    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'negocio_origen':lv_negocio, 'enviado_por':self.request.user}
    
    # Validar formulario antes de guardar
    def form_valid(self, form):
        obj = form.save(commit=False)

        # el negocio se pasa en el initial según el usuario logueado
        if obj.negocio_origen is None:
            obj.negocio_origen = self.request.user.relPerfilUsuario.negocio
        
        # el negocio se pasa en el initial según el usuario logueado
        if obj.enviado_por is None:
            obj.enviado_por = self.request.user

        return super(EncabezadoMensajeCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('mensajeria_encabezado_list')


# 1.2. Actualizar EncabezadoMensaje
class EncabezadoMensajeUpdateView(LoginRequiredMixin, UpdateView):
    model = m_mensajeria.EncabezadoMensaje
    form_class = f_mensajeria.EncabezadoMensajeUpdateModelForm
    template_name = 'mensajeria/encabezado_mensaje_add.html'

    def get_context_data(self, **kwargs):
        context = super(EncabezadoMensajeUpdateView, self).get_context_data(**kwargs)

        context['hilo_mensajes_list'] = m_mensajeria.HiloMensaje.objects.filter(encabezado_mensaje = self.object)

        lv_negocio = self.request.user.relPerfilUsuario.negocio
        context['hilo_mensaje_form'] = f_mensajeria.HiloMensajeModelForm(initial={
                                                                            'encabezado_mensaje':self.object,
                                                                            'enviado_por':self.request.user,
                                                                            'negocio_origen':lv_negocio
                                                                            }
                                                                        )

        return context
    
    # Validar formulario antes de guardar
    def form_valid(self, form):
        obj = form.save(commit=False)

        # el negocio se pasa en el initial según el usuario logueado
        if obj.negocio_origen is None:
            obj.negocio_origen = self.request.user.relPerfilUsuario.negocio
        
        # el negocio se pasa en el initial según el usuario logueado
        if obj.enviado_por is None:
            obj.enviado_por = self.request.user
        
        return super(EncabezadoMensajeUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('mensajeria_encabezado_list')


# 1.3. Lista de EncabezadoMensaje
class EncabezadoMensajeListView(ListView):
    model = m_mensajeria.EncabezadoMensaje
    paginate_by = 100
    template_name = 'mensajeria/mensajeria_encabezado_list.html'

    def get_queryset(self):
        queryset = super(EncabezadoMensajeListView, self).get_queryset()
        
        lv_negocio=None
        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        return queryset.filter(Q(negocio_origen=lv_negocio) | Q(negocio_destino=lv_negocio))

"""
    **************************************************
    ./Encabezado de Mensajes
    **************************************************
"""






"""
    **************************************************
    Hilo de Mensajes
    **************************************************
"""
# 1.2. Agregar HiloMensaje
class HiloMensajeCreateView(LoginRequiredMixin, CreateView):
    model = m_mensajeria.HiloMensaje
    form_class = f_mensajeria.HiloMensajeModelForm
    template_name = 'mensajeria/hilo_mensaje_add.html'

    # Inicializar los valores del formulario
    def get_initial(self):
        if self.request.user:
            lv_usuario = self.request.user
            lv_negocio = self.request.user.relPerfilUsuario.negocio
        return { 'enviado_por':lv_usuario, 'negocio_origen':lv_negocio }
    
    # Validar formulario antes de guardar
    def form_valid(self, form):
        obj = form.save(commit=False)

        # el usuario se pasa en el initial según el usuario logueado
        if obj.enviado_por is None:
            obj.enviado_por = self.request.user
        
        # el negocio se pasa en el initial según el usuario logueado
        if obj.negocio_origen is None:
            obj.negocio_origen = self.request.user.relPerfilUsuario.negocio

        return super(HiloMensajeCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse('mensajeria_encabezado_update', kwargs={'pk':self.object.encabezado_mensaje.id})


# 1.2. Actualizar HiloMensaje
class HiloMensajeUpdateView(LoginRequiredMixin, UpdateView):
    model = m_mensajeria.HiloMensaje
    form_class = f_mensajeria.HiloMensajeUpdateModelForm
    template_name = 'mensajeria/hilo_mensaje_update.html'

    def get_context_data(self, **kwargs):
        context = super(HiloMensajeUpdateView, self).get_context_data(**kwargs)

        context['hilo_mensajes_list'] = m_mensajeria.HiloMensaje.objects.filter(encabezado_mensaje = self.object.encabezado_mensaje)

        return context
        
    def get_success_url(self):
        return reverse('mensajeria_encabezado_update', kwargs={'pk':self.object.encabezado_mensaje.id})

"""
    **************************************************
    ./Hilo de Mensajes
    **************************************************
"""