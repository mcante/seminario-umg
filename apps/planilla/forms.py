from django import forms
from django.forms import ModelForm

from apps.planilla import models as m_planilla

# EMPLEADOS ADD AND UPDATE
class EmpleadosModelForm(forms.ModelForm):
    class Meta:
        model = m_planilla.Empleados
        fields = '__all__'
        widgets = {
            'email' : forms.TextInput(attrs={'placeholder': 'ejemplo@gmail.com', 'data-parsley-trigger': 'change'}),
            'fecha_ingreso': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'fecha_terminacion': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'puesto': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            #'activo' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            
        }


# ENCABEZADO PLANILLA ADD AND UPDATE
class EncabezadoPlanillaModelForm(forms.ModelForm):
    class Meta:
        model = m_planilla.EncabezadoPlanilla
        fields = '__all__'
        widgets = {
            'tipo_pago': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'mes': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            #'generar_automaticamente' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            #'ha_sido_generado' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'ha_sido_generado': forms.HiddenInput(),
            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
        }

# PLANILLA ADD AND UPDATE
class PlanillaModelForm(forms.ModelForm):
    class Meta:
        model = m_planilla.Planilla
        fields = '__all__'
        widgets = {
            'encabezado_planilla': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'empleado': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'tipo_pago': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'mes': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            
            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
        }
    