from django import forms

from django.forms import ModelForm
from django.contrib.auth.models import User
from apps.registration.models import Negocio, Perfil
from apps.clientes.models import Cliente, NegocioCliente, Contacto
from apps.factura.models import Pedido, EstadoPedido

"""
    CLIENTES
"""
class ClienteForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        #exclude = ['estado', 'prioridad', 'departamento', 'agente', 'cerrado', 'creado', 'actualizado', 'creado_por']
        widgets = {
            'email' : forms.TextInput(attrs={'placeholder': 'ejemplo@gmail.com', 'data-parsley-trigger': 'change'}),
            'telefono' : forms.TextInput(attrs={'placeholder': '22224444'}),
            'nit' : forms.TextInput(attrs={'placeholder': 'Número de Nit'}),
            'direccion': forms.Textarea(attrs={"rows":"3"}),
            'empleado_asignado': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            #'clasificacion': forms.Select(attrs={'class': 'select2bs4'}),
            'key_access': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
    
    def __init__(self, *args, **kwargs):
        p_negocio = kwargs.pop('p_negocio')
        
        super(ClienteForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['empleado_asignado'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__negocio=p_negocio, relPerfilUsuario__tipo_empleado=1) # tipo_empleado = 1 = VENDEDOR
        self.fields['empleado_asignado'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())
        

class ClienteUpdateForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            'email' : forms.TextInput(attrs={'placeholder': 'ejemplo@gmail.com', 'data-parsley-trigger': 'change'}),
            'telefono' : forms.TextInput(attrs={'placeholder': '22224444'}),
            'nit' : forms.TextInput(attrs={'placeholder': 'Número de Nit'}),
            'direccion': forms.Textarea(attrs={"rows":"3"}),
            'key_access': forms.TextInput(attrs={'placeholder': ''}),
            'empleado_asignado': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            #'clasificacion': forms.Select(attrs={'class': 'select2bs4'}),
            
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
    

    def __init__(self, *args, **kwargs):
        p_negocio = kwargs.pop('p_negocio')
        
        super(ClienteUpdateForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['empleado_asignado'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__negocio=p_negocio, relPerfilUsuario__tipo_empleado=1) # tipo_empleado = 1 = VENDEDOR
        self.fields['empleado_asignado'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())




class ClientePublicoForm(forms.ModelForm):
    class Meta:
        model = Cliente
        fields = '__all__'
        widgets = {
            
            'email': forms.HiddenInput(),
            'telefono': forms.HiddenInput(),
            'nit': forms.HiddenInput(),
            'direccion': forms.HiddenInput(),
            'empleado_asignado': forms.HiddenInput(),

            'key_access': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
    

"""
   ./ CLIENTES
"""


"""
    NegocioCliente
"""
class NegocioClienteForm(forms.ModelForm):
    class Meta:
        model = NegocioCliente
        fields = '__all__'
        widgets = {
            'negocio': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'cliente': forms.HiddenInput(),
            'vendedor': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
        }
    
    def __init__(self, p_cliente=None, *args, **kwargs):
        p_obj_cliente = p_cliente
        #print(p_obj_cliente)

        super(NegocioClienteForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        ObjNegociosAsignados = NegocioCliente.objects.filter(cliente=p_obj_cliente).values_list('negocio')
        self.fields['negocio'].queryset = Negocio.objects.exclude(id__in=ObjNegociosAsignados)
        self.fields['negocio'].label_from_instance = lambda obj: "%s" % (obj.nombre_negocio)

        self.fields['vendedor'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())

"""
    ./ NegocioCliente
"""




"""
    CONTACTO
"""

class ContactoUpdateForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = '__all__'
        widgets = {
            'negocio': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'email' : forms.TextInput(attrs={'placeholder': 'ejemplo@gmail.com', 'data-parsley-trigger': 'change'}),
            'telefono' : forms.TextInput(attrs={'placeholder': '22224444'}),
            'mensaje': forms.Textarea(attrs={"rows":"3"}),
            
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
    

class ContactoPublicoForm(forms.ModelForm):
    class Meta:
        model = Contacto
        fields = '__all__'
        widgets = {

            'negocio': forms.Select(attrs={'class': 'form-control', 'style':'width: 100%;'}),
            'nombre_contacto' : forms.TextInput(attrs={'placeholder': 'Nombre'}),
            'email' : forms.TextInput(attrs={'placeholder': 'Correo', 'data-parsley-trigger': 'change'}),            
            'telefono' : forms.TextInput(attrs={'placeholder': '22224444'}),
            'nombre_empresa' : forms.TextInput(attrs={'placeholder': 'Empresa'}),
            'mensaje': forms.Textarea(attrs={"rows":"3", 'placeholder': 'Mensaje'}),
            
            'atentido': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
    

"""
   ./ CONTACTO
"""





"""
    PEDIDOS PÁGINAS CLIENTES PUBLICO
    -----------------------------------
"""
class PedidoAddPublicForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = '__all__'
        widgets = {
            #'cliente': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            #'fecha_pedido': forms.DateInput(attrs={'class': 'DataPicker', 'placeholder': 'dd/mm/aaaa'}),
            'descripcion_detalle_pedido': forms.Textarea(attrs={"rows":"5", 'required':True}),
            'negocio': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;', 'required':True}),
            #'vendedor': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            #'estado_pedido': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            #'anotaciones_seguimiento': forms.Textarea(attrs={"rows":"3"}),
            #'completado' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'cliente': forms.HiddenInput(),
            'fecha_pedido': forms.HiddenInput(),
            'vendedor': forms.HiddenInput(),
            'estado_pedido': forms.HiddenInput(),
            'anotaciones_seguimiento': forms.HiddenInput(),
            'completado': forms.HiddenInput(),

            
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
    

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
    
"""
    PEDIDOS PÁGINAS CLIENTES PUBLICO
    -----------------------------------
"""




"""
FILTROS PARA EL CONSUMO REST
=================================================
"""

class ClienteRestForm(forms.Form):
    """Formulario que Controla los filtros para poder hacer busquedas
    """
    
    id_cliente = forms.CharField(
        label='Código Cliente',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    
    nombre_empresa = forms.CharField(
        label='Nombre de Empresa',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    
    email = forms.CharField(
        label='Correo',
        required=False,
        widget=forms.EmailInput(attrs={'class': 'form-control form-control-sm'}))
    
    telefono = forms.CharField(
        label='Teléfono',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    
    nit = forms.CharField(
        label='Nit Empresa',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))

    empleado_asignado = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label='Usuario o Correo',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm select2bs4'}))
    
    def __init__(self, *args, **kwargs):
        super(ClienteRestForm, self).__init__(*args, **kwargs)
        self.fields['empleado_asignado'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())
        
        