from django import forms
from django.forms import ModelForm

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from apps.factura.models import EstadoFactura, EstadoVenta, Pedido, Factura, EstadoDespacho, Despacho
from apps.clientes.models import Cliente
from apps.registration.models import Negocio


"""
    PEDIDOS PÁGINAS ADMINISTRATIVAS
    -----------------------------------
"""
class PedidoAddAdminForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
        widgets = {
            'cliente': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            #'fecha_pedido': forms.DateInput(attrs={'class': 'DataPicker', 'placeholder': 'dd/mm/aaaa'}),
            'descripcion_detalle_pedido': forms.Textarea(attrs={"rows":"3"}),
            #'vendedor': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            #'estado_pedido': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            #'anotaciones_seguimiento': forms.Textarea(attrs={"rows":"3"}),
            #'completado' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'fecha_pedido': forms.HiddenInput(),
            'vendedor': forms.HiddenInput(),
            'estado_pedido': forms.HiddenInput(),
            'anotaciones_seguimiento': forms.HiddenInput(),
            'completado': forms.HiddenInput(),

            'negocio': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
    
    def __init__(self, *args, **kwargs):
        p_negocio = kwargs.pop('p_negocio') # Aun no implementado para validar la lista de vendedores asociados con el cliente.
        
        super(PedidoAddAdminForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        #self.fields['vendedor'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__relNegocioUsuarioPerfil__negocio__in=p_negocio, relPerfilUsuario__tipo_empleado=1) # tipo_empleado = 1 = VENDEDOR
        self.fields['vendedor'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=1) # tipo_empleado = 1 = VENDEDOR
        self.fields['vendedor'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())

        self.fields['cliente'].queryset = Cliente.objects.filter(relNegocioClienteCliente__negocio=p_negocio)
        self.fields['cliente'].label_from_instance = lambda obj: "%s" % (obj.nombre_empresa)


class PedidoUpdateAdminForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
        widgets = {
            #'cliente': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            #'fecha_pedido': forms.DateInput(attrs={'class': 'DataPicker', 'placeholder': 'dd/mm/aaaa'}),
            #'descripcion_detalle_pedido': forms.Textarea(attrs={"rows":"3"}),
            'vendedor': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'estado_pedido': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'anotaciones_seguimiento': forms.Textarea(attrs={"rows":"3"}),
            'completado' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'cliente': forms.HiddenInput(),
            'fecha_pedido': forms.HiddenInput(),
            #'estado_pedido': forms.HiddenInput(),
            'descripcion_detalle_pedido': forms.HiddenInput(),
            #'completado': forms.HiddenInput(),

            'negocio': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
    
    def __init__(self, *args, **kwargs):
        p_negocio = kwargs.pop('p_negocio') # Aun no implementado para validar la lista de vendedores asociados con el cliente.
        
        super(PedidoUpdateAdminForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        #self.fields['vendedor'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__relNegocioUsuarioPerfil__negocio__in=p_negocio, relPerfilUsuario__tipo_empleado=1) # tipo_empleado = 1 = VENDEDOR
        self.fields['vendedor'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=1) # tipo_empleado = 1 = VENDEDOR
        self.fields['vendedor'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())

        self.fields['cliente'].queryset = Cliente.objects.filter(relNegocioClienteCliente__negocio=p_negocio)
        self.fields['cliente'].label_from_instance = lambda obj: "%s" % (obj.nombre_empresa)

"""
    PEDIDOS PÁGINAS ADMINISTRATIVAS
    -----------------------------------
"""






"""
    FACTURA
    -----------------------------------
"""
class FacturaCreateForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'
        widgets = {
            'cliente': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'pedido': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'fecha_factura': forms.DateInput(attrs={'class': 'DataPicker', 'placeholder': 'dd/mm/aaaa'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'vendedor': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            'estado_factura': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'tipo_pago': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'estado_venta': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            'numero_factura': forms.HiddenInput(),
            'completado': forms.HiddenInput(),
            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
    
    def __init__(self, *args, **kwargs):
        p_negocio = kwargs.pop('p_negocio', None) # Aun no implementado para validar la lista de vendedores asociados con el cliente.

        super(FacturaCreateForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        #self.fields['vendedor'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__relNegocioUsuarioPerfil__negocio__in=p_negocio, relPerfilUsuario__tipo_empleado=1) # tipo_empleado = 1 = VENDEDOR
        self.fields['vendedor'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=1) # tipo_empleado = 1 = VENDEDOR
        self.fields['vendedor'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())

        if(p_negocio):
            self.fields['cliente'].queryset = Cliente.objects.filter(relNegocioClienteCliente__negocio=p_negocio)
            self.fields['cliente'].label_from_instance = lambda obj: "%s" % (obj.nombre_empresa)
        else:
            self.fields['cliente'].queryset = Cliente.objects.all()
            self.fields['cliente'].label_from_instance = lambda obj: "%s" % (obj.nombre_empresa)
    

class FacturaUpdateForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'
        widgets = {
            'cliente': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'pedido': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'fecha_factura': forms.DateInput(attrs={'class': 'DataPicker', 'placeholder': 'dd/mm/aaaa'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'vendedor': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            'estado_factura': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'tipo_pago': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'estado_venta': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            'numero_factura': forms.HiddenInput(),
            'completado': forms.HiddenInput(),
            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
    
    def __init__(self, *args, **kwargs):
        p_negocio = kwargs.pop('p_negocio', None) # Aun no implementado para validar la lista de vendedores asociados con el cliente.

        super(FacturaUpdateForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        #self.fields['vendedor'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__relNegocioUsuarioPerfil__negocio__in=p_negocio, relPerfilUsuario__tipo_empleado=1) # tipo_empleado = 1 = VENDEDOR
        self.fields['vendedor'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=1) # tipo_empleado = 1 = VENDEDOR
        self.fields['vendedor'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())

        if(p_negocio):
            self.fields['cliente'].queryset = Cliente.objects.filter(relNegocioClienteCliente__negocio=p_negocio)
            self.fields['cliente'].label_from_instance = lambda obj: "%s" % (obj.nombre_empresa)
        else:
            self.fields['cliente'].queryset = Cliente.objects.all()
            self.fields['cliente'].label_from_instance = lambda obj: "%s" % (obj.nombre_empresa)
    
"""
    FACTURA
    -----------------------------------
"""





"""
    Despacho
"""
class DespachoForm(forms.ModelForm):
    class Meta:
        model = Despacho
        fields = '__all__'
        widgets = {
            'factura': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'fecha_despacho': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'persona_recibe' : forms.TextInput(attrs={'placeholder': 'Persona que recibe'}),
            'empleado': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'anotaciones_despacho': forms.Textarea(attrs={"rows":"3"}),
            'estado_despacho': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'completado' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            
        }
    def __init__(self, *args, **kwargs):
        p_negocio = kwargs.pop('p_negocio', None) # Aun no implementado para validar la lista de vendedores asociados con el cliente.

        super(DespachoForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['factura'].queryset = Factura.objects.filter(negocio=p_negocio, estado_factura = 2) # 2 = estado_factura = Lista para entregar
        self.fields['factura'].label_from_instance = lambda obj: "#%s / fecha: %s" % (obj.numero_factura, obj.fecha_factura)

        self.fields['empleado'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=1, relPerfilUsuario__negocio=p_negocio) # 1 VENDEDOR
        self.fields['empleado'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())
    

class DespachoUpdateForm(forms.ModelForm):
    class Meta:
        model = Despacho
        fields = '__all__'
        widgets = {
            'factura': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'fecha_despacho': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'persona_recibe' : forms.TextInput(attrs={'placeholder': 'Persona que recibe'}),
            'empleado': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'anotaciones_despacho': forms.Textarea(attrs={"rows":"3"}),
            'estado_despacho': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'completado' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            
        }
    def __init__(self, *args, **kwargs):
        p_negocio = kwargs.pop('p_negocio', None) # Aun no implementado para validar la lista de vendedores asociados con el cliente.

        super(DespachoUpdateForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['factura'].queryset = Factura.objects.filter(completada=False, negocio=p_negocio)
        self.fields['factura'].label_from_instance = lambda obj: "#%s / fecha: %s" % (obj.numero_factura, obj.fecha_factura)

        self.fields['empleado'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=1, relPerfilUsuario__negocio=p_negocio) # 1 VENDEDOR
        self.fields['empleado'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())
    

"""
   ./ Despacho
"""





"""
FILTROS PARA EL CONSUMO REST
=================================================
"""

"""
    FILTROS FACTURAS
"""
class FacturaRestForm(forms.Form):
    """Formulario que Controla los filtros para poder hacer busquedas
    """
    CONFIRMACION_CHOICES = (
        (None, 'Ambos'),
        ('1', 'Sí'),
        ('0', 'No'))
    
    numero_factura = forms.CharField(
        label='Número de Factura',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    
    cliente = forms.ModelChoiceField(
        queryset=Cliente.objects.all(),
        label='Cliente',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm select2bs4'}))
    
    # Fecha de Factura
    fecha_factura_min = forms.CharField(
        label='Fecha Factura (Inicio)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm datepicker'}))
    fecha_factura_max = forms.CharField(
        label='Fecha Factura (Final)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm datepicker'}))
    
    vendedor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label='Vendedor',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm select2bs4'}))
    
    estado_factura = forms.ModelChoiceField(
        queryset=EstadoFactura.objects.all(),
        label='Estado Factura',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm select2bs4'}))
    
    estado_venta = forms.ModelChoiceField(
        queryset=EstadoVenta.objects.all(),
        label='Estado Venta',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm select2bs4'}))
    
    completada = forms.ChoiceField(
        choices=CONFIRMACION_CHOICES,
        label='Facturas Completadas',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2bs4',}))

    def __init__(self, *args, **kwargs):
        super(FacturaRestForm, self).__init__(*args, **kwargs)
        self.fields['vendedor'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=1) # tipo_empleado = 1 = VENDEDOR
        self.fields['vendedor'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())
        




"""
    FILTROS VENTAS
"""
class VentasRestForm(forms.Form):
    """Formulario que Controla los filtros para poder hacer busquedas
    """
    
    fecha_registro_min = forms.CharField(
        label='Fecha Venta (Inicio)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm datepicker'}))
    fecha_registro_max = forms.CharField(
        label='Fecha Venta (Final)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm datepicker'}))
    


"""
    FILTROS VENTAS GLOABL
"""
class VentasGlobalRestForm(forms.Form):
    """Formulario que Controla los filtros para poder hacer busquedas
    """
    
    fecha_registro_min = forms.CharField(
        label='Fecha Venta (Inicio)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm datepicker'}))
    fecha_registro_max = forms.CharField(
        label='Fecha Venta (Final)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm datepicker'}))
    negocio = forms.ModelChoiceField(
        queryset=Negocio.objects.all(),
        label='Negocio',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm select2bs4'}))

    def __init__(self, *args, **kwargs):
        
        super(VentasGlobalRestForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['negocio'].label_from_instance = lambda obj: "%s" % (obj.nombre_negocio)



"""
    FILTROS FACTURAS PUBLICO
"""

class PedidoPublicoRestForm(forms.Form):
    """Formulario que Controla los filtros para poder hacer busquedas
    """
    id = forms.CharField(
        label='No. Pedido',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    
    fecha_pedido_min = forms.CharField(
        label='Fecha Pedido (Inicio)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm datepicker'}))
    fecha_pedido_max = forms.CharField(
        label='Fecha Pedido (Final)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm datepicker'}))
    
    negocio = forms.ModelChoiceField(
        queryset=Negocio.objects.all(),
        label='Negocio',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm select2bs4'}))
    
    completado = forms.CharField(
        label='Pedido Completado',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-control form-control-sm'}))







class FacturaPublicoRestForm(forms.Form):
    """Formulario que Controla los filtros para poder hacer busquedas
    """
    CONFIRMACION_CHOICES = (
        (None, 'Ambos'),
        ('1', 'Sí'),
        ('0', 'No'))
        
    numero_factura = forms.CharField(
        label='Número de Factura',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    
    # Fecha de Factura
    fecha_factura_min = forms.CharField(
        label='Fecha Factura (Inicio)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm datepicker'}))
    fecha_factura_max = forms.CharField(
        label='Fecha Factura (Final)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm datepicker'}))
    
    vendedor = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label='Vendedor',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm select2bs4'}))
    
    estado_factura = forms.ModelChoiceField(
        queryset=EstadoFactura.objects.all(),
        label='Estado Factura',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm select2bs4'}))
    
    negocio = forms.ModelChoiceField(
        queryset=Negocio.objects.all(),
        label='Negocio',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm select2bs4'}))
    
    completada = forms.ChoiceField(
        choices=CONFIRMACION_CHOICES,
        label='Facturas Completadas',
        required=False,
        widget=forms.Select(attrs={'class': 'form-control select2bs4',}))
    
    def __init__(self, *args, **kwargs):
        super(FacturaPublicoRestForm, self).__init__(*args, **kwargs)
        self.fields['vendedor'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=1) # tipo_empleado = 1 = VENDEDOR
        self.fields['vendedor'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())
        




class DespachoPublicoRestForm(forms.Form):
    """Formulario que Controla los filtros para poder hacer busquedas
    """
    
    fecha_despacho_min = forms.CharField(
        label='Fecha Despacho (Inicio)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm datepicker'}))
    fecha_despacho_max = forms.CharField(
        label='Fecha Despacho (Final)',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm datepicker'}))
    
    empleado = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label='Empleado',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm select2bs4'}))
    
    estado_despacho = forms.ModelChoiceField(
        queryset=EstadoDespacho.objects.all(),
        label='Estado Despacho',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm select2bs4'}))
    
    negocio = forms.ModelChoiceField(
        queryset=Negocio.objects.all(),
        label='Negocio',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm select2bs4'}))
    
    completado = forms.CharField(
        label='Despacho Completado',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-control form-control-sm'}))
    
    def __init__(self, *args, **kwargs):
        super(DespachoPublicoRestForm, self).__init__(*args, **kwargs)
        self.fields['empleado'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=1) # tipo_empleado = 1 = VENDEDOR
        self.fields['empleado'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())
        

