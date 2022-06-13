from django import forms
from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import TipoGasto, RegistroGastos
from apps.registration import models as m_registration



"""
    PEDIDOS PÁGINAS ADMINISTRATIVAS
    -----------------------------------
"""
class RegistroGastosModelForm(forms.ModelForm):
    class Meta:
        model = RegistroGastos
        fields = '__all__'
        widgets = {
            'tipo_gasto': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'fecha_gasto': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control-sm'}),
            'descripcion_gasto': forms.Textarea(attrs={"rows":"3"}),
            'autorizado_por': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'negocio': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            
        }
    
    
    def __init__(self, *args, **kwargs):
        p_negocio = kwargs.pop('p_negocio') # Aun no implementado para validar la lista de vendedores asociados con el cliente.
        
        super(RegistroGastosModelForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['tipo_gasto'].queryset = TipoGasto.objects.filter(negocio=p_negocio) # tipo_empleado = 1 = VENDEDOR
        self.fields['tipo_gasto'].label_from_instance = lambda obj: "%s" % (obj.nombre_gasto)

        self.fields['autorizado_por'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=2, relPerfilUsuario__negocio=p_negocio) # tipo_empleado = 2 = ADMINISTRATIVO
        self.fields['autorizado_por'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())



class RegistroUpdateGastosModelForm(forms.ModelForm):
    class Meta:
        model = RegistroGastos
        fields = '__all__'
        widgets = {
            #'tipo_gasto': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            #'fecha_gasto': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            #'monto': forms.NumberInput(attrs={'class': 'form-control-sm'}),
            'descripcion_gasto': forms.Textarea(attrs={"rows":"3"}),
            #'autorizado_por': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            

            'tipo_gasto': forms.HiddenInput(),
            'fecha_gasto': forms.HiddenInput(),
            'monto': forms.HiddenInput(),
            'autorizado_por': forms.HiddenInput(),

            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            
        }




"""
    FILTROS Registro Gastos
"""
class RegistroGastosRestForm(forms.Form):
    """Formulario que Controla los filtros para poder hacer busquedas
    """

    tipo_gasto = forms.ModelChoiceField(
        queryset=TipoGasto.objects.all(),
        label='Tipo de Gasto',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm select2bs4'}))
    
    fecha_registro_min = forms.CharField(
        label='Fecha Venta (Inicio)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm datepicker'}))
    fecha_registro_max = forms.CharField(
        label='Fecha Venta (Final)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm datepicker'}))
    
    autorizado_por = forms.ModelChoiceField(
        queryset=User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=2), # tipo_empleado = 2 = ADMINISTRATIVO
        label='Autorizado por',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm select2bs4'}))
    
    def __init__(self, *args, **kwargs):
        p_negocio = kwargs.pop('p_negocio', None)
        
        super(RegistroGastosRestForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['autorizado_por'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=2, relPerfilUsuario__relNegocioUsuarioPerfil__negocio=p_negocio) # tipo_empleado = 2 = ADMINISTRATIVO
        self.fields['autorizado_por'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())

        self.fields['tipo_gasto'].queryset = TipoGasto.objects.filter(negocio=p_negocio)
        self.fields['tipo_gasto'].label_from_instance = lambda obj: "%s" % (obj.nombre_gasto)




"""
    FILTROS Registro Gastos Global
"""
class RegistroGastosGlobalRestForm(forms.Form):
    """Formulario que Controla los filtros para poder hacer busquedas
    """

    tipo_gasto = forms.ModelChoiceField(
        queryset=TipoGasto.objects.all(),
        label='Tipo de Gasto',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm select2bs4'}))
    
    fecha_registro_min = forms.CharField(
        label='Fecha Venta (Inicio)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm datepicker'}))
    fecha_registro_max = forms.CharField(
        label='Fecha Venta (Final)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm datepicker'}))
    
    autorizado_por = forms.ModelChoiceField(
        queryset=User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=2), # tipo_empleado = 2 = ADMINISTRATIVO
        label='Autorizado por',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm select2bs4'}))
    negocio = forms.ModelChoiceField(
        queryset=m_registration.Negocio.objects.all(),
        label='Negocio',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm select2bs4'}))
    
    def __init__(self, *args, **kwargs):
        
        super(RegistroGastosGlobalRestForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['autorizado_por'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=2) # tipo_empleado = 2 = ADMINISTRATIVO
        self.fields['autorizado_por'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())

        self.fields['tipo_gasto'].label_from_instance = lambda obj: "%s (%s)" % (obj.nombre_gasto, obj.negocio.nombre_negocio)

        self.fields['negocio'].label_from_instance = lambda obj: "%s" % (obj.nombre_negocio)