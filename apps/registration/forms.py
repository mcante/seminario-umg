from django import forms

from django.forms import ModelForm
from apps.registration.models import Presupuesto


"""
    Presupuesto
"""
class PresupuestoForm(forms.ModelForm):
    class Meta:
        model = Presupuesto
        fields = '__all__'
        widgets = {
            'presupuesto_anual': forms.NumberInput(attrs={'class': 'form-control'}),
            'excedente': forms.NumberInput(attrs={'class': 'form-control'}),
            'anio': forms.NumberInput(attrs={'class': 'form-control'}),

            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
    
"""
    ./Presupuesto
"""
