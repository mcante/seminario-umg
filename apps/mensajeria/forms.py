from django import forms
from django.forms import ModelForm

from apps.mensajeria import models as m_mensajeria
from apps.registration import models as m_registration

# ENCABEZADO MENSAJE ADD
class EncabezadoMensajeModelForm(forms.ModelForm):
    class Meta:
        model = m_mensajeria.EncabezadoMensaje
        fields = '__all__'
        widgets = {
            'mensaje': forms.Textarea(attrs={"rows":"3"}),
            'negocio_destino': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            'enviado_por': forms.HiddenInput(),
            'negocio_origen': forms.HiddenInput(),            
        }
    
    def __init__(self, *args, **kwargs):
        p_negocio = kwargs.pop('p_negocio')

        super(EncabezadoMensajeModelForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['negocio_destino'].queryset = m_registration.Negocio.objects.exclude(id=p_negocio.id)
        self.fields['negocio_destino'].label_from_instance = lambda obj: "%s" % (obj.nombre_negocio)


# ENCABEZADO MENSAJE UPDATE
class EncabezadoMensajeUpdateModelForm(forms.ModelForm):
    class Meta:
        model = m_mensajeria.EncabezadoMensaje
        fields = '__all__'
        widgets = {
            
            'mensaje': forms.HiddenInput(),
            'enviado_por': forms.HiddenInput(),
            'negocio_origen': forms.HiddenInput(),            
            'negocio_destino': forms.HiddenInput(),
        }



# MENSAJE ADD
class HiloMensajeModelForm(forms.ModelForm):
    class Meta:
        model = m_mensajeria.HiloMensaje
        fields = '__all__'
        widgets = {
            'mensaje': forms.Textarea(attrs={"rows":"3"}),
            'negocio_destino': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            'encabezado_mensaje': forms.HiddenInput(),
            'mensaje_leido': forms.HiddenInput(),
            'negocio_origen': forms.HiddenInput(),
            'negocio_destino': forms.HiddenInput(),
            'enviado_por': forms.HiddenInput(),            
        }
    
# MENSAJE UPDATE
class HiloMensajeUpdateModelForm(forms.ModelForm):
    class Meta:
        model = m_mensajeria.HiloMensaje
        fields = '__all__'
        widgets = {
            
            'encabezado_mensaje': forms.HiddenInput(),
            'mensaje': forms.HiddenInput(),
            'negocio_origen': forms.HiddenInput(),
            'negocio_destino': forms.HiddenInput(),            
            'enviado_por': forms.HiddenInput(),
        }

