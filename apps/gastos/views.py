from django.shortcuts import render

from django.views.generic import UpdateView, DetailView, ListView, CreateView, FormView, TemplateView, View
from django.urls import reverse_lazy, reverse

import datetime
from django.utils import timezone

# Decoradores para validar permisos de autenticación y grupos
from django.contrib.auth.mixins import LoginRequiredMixin
from braces.views import GroupRequiredMixin

# FORMS
from .forms import RegistroGastosModelForm, RegistroUpdateGastosModelForm, RegistroGastosRestForm, RegistroGastosGlobalRestForm

# MODELOS
from django.contrib.auth.models import User
from .models import RegistroGastos, TipoGasto
#from apps.registration.models import NegocioCliente



# REST
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.response import Response

# Serializadores y filtros para REST
from apps.gastos.serializers import RegistroGastosModelSerializer
from apps.gastos.filters import RegistroGastosFilterSet




"""
********************** LISTA DE ESPERA **********************
    LISTA DE ESPERA - Crear
"""

# Agregar RegistroGastos
class RegistroGastosCreateView(GroupRequiredMixin, LoginRequiredMixin, CreateView):
    group_required = [u"Administrativo", u"Contador", u"Operativo"]
    model = RegistroGastos
    form_class = RegistroGastosModelForm
    template_name = 'gastos/gastos_add.html'


    # Validar formulario antes de guardar
    def form_valid(self, form):
        obj = form.save(commit=False)

        obj.creado_por = self.request.user

        return super(RegistroGastosCreateView, self).form_valid(form)


    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(RegistroGastosCreateView, self).get_form_kwargs()

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

    def get_success_url(self):
        return reverse('gastos_update', kwargs={'pk':self.object.id})



"""
    LISTA DE ESPERA - Actualizar
"""    
# Actuaizar RegistroGastos
class RegistroGastosUpdateView(GroupRequiredMixin, LoginRequiredMixin, UpdateView):
    group_required = [u"Administrativo", u"Contador", u"Operativo"]
    model = RegistroGastos
    form_class = RegistroUpdateGastosModelForm
    template_name = 'gastos/gastos_add.html'

    # Validar formulario antes de guardar
    def form_valid(self, form):
        obj = form.save(commit=False)

        obj.actualizado_por = self.request.user

        return super(RegistroGastosUpdateView, self).form_valid(form)

    # Después de guardar, redireccionará a la URL indicada
    def get_success_url(self):
        #return reverse('lista_espera_filter_list')
        return reverse('gastos_update', kwargs={'pk':self.object.id})

"""
********************** ./LISTA DE ESPERA **********************
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
class RegistroGastosListAPIView(ListAPIView):
    serializer_class = RegistroGastosModelSerializer
    queryset = RegistroGastos.objects.all()
    filter_class = RegistroGastosFilterSet
    pagination_class = ResultsSetPagination

# 1.2: Muestra los filtros en el template para ejecutar el API y cargar los resultados con Ajax desde el template
class RegistroGastosFormView(GroupRequiredMixin, LoginRequiredMixin, FormView):
    group_required = [u"Administrativo", u"Contador", u"Operativo"]
    model = RegistroGastos
    form_class = RegistroGastosRestForm
    template_name = 'gastos/gastos_filter_list.html'

    # Pasa los parametros al formulario para filtrar los combobox
    def get_form_kwargs(self, *args, **kwargs):
        kwargs = super(RegistroGastosFormView, self).get_form_kwargs()

        lv_negocio=None

        if self.request.user:
            lv_negocio = self.request.user.relPerfilUsuario.negocio

        kwargs['p_negocio'] = lv_negocio

        return kwargs


# 1.3: Muestra los filtros en el template para ejecutar el API y cargar los resultados con Ajax desde el template
class RegistroGastosGlobalFormView(GroupRequiredMixin, LoginRequiredMixin, FormView):
    group_required = [u"Administrativo"]
    model = RegistroGastos
    form_class = RegistroGastosGlobalRestForm
    template_name = 'gastos/gastos_filter_global_list.html'
