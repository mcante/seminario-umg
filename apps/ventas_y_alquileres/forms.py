from django import forms

from django.forms import ModelForm
from django.contrib.auth.models import User
from apps.registration.models import Negocio, Perfil

from .models import Marca, TipoMaquina, Maquina, InventarioMaquinariaVentas, \
IngresoCompras, InventarioMaquinariaAlquiler, EstadoAlquiler, AlquilerMaquina, DetalleFactura


from apps.proveedores.models import Proveedor
from apps.factura.models import Factura, Pedido
from apps.clientes.models import Cliente






"""
    Maquina
    -----------------------------------
"""
class MaquinaCreateForm(forms.ModelForm):
    class Meta:
        model = Maquina
        fields = '__all__'
        widgets = {
            'marca': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'proveedor': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'tipo_maquina': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'descripcion': forms.Textarea(attrs={"rows":"3"}),

            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
    
    def __init__(self, *args, **kwargs):
        p_negocio_form = kwargs.pop('p_negocio', None)

        super(MaquinaCreateForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['proveedor'].queryset = Proveedor.objects.filter(negocio=p_negocio_form) 
        self.fields['proveedor'].label_from_instance = lambda obj: "%s" % (obj.nombre_proveedor)

        self.fields['marca'].label_from_instance = lambda obj: "%s" % (obj.nombre)
    
"""
    Maquina
    -----------------------------------
"""






"""
    InventarioMaquinariaVentas
    -----------------------------------
"""
class InventarioMaquinariaVentasCreateForm(forms.ModelForm):
    class Meta:
        model = InventarioMaquinariaVentas
        fields = '__all__'
        widgets = {
            'maquina': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_maquina': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            
            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
    
    
    def __init__(self, *args, **kwargs):
        p_negocio_form = kwargs.pop('p_negocio', None)

        super(InventarioMaquinariaVentasCreateForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['maquina'].queryset = Maquina.objects.filter(negocio=p_negocio_form) 
        self.fields['maquina'].label_from_instance = lambda obj: "%s" % (obj.nombre)
    
    
"""
    InventarioMaquinariaVentas
    -----------------------------------
"""






"""
    IngresoCompras
    -----------------------------------
"""
class IngresoComprasCreateForm(forms.ModelForm):
    class Meta:
        model = IngresoCompras
        fields = '__all__'
        widgets = {
            'fecha_compra': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'maquina': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_maquina': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            
            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
    
    
    def __init__(self, *args, **kwargs):
        p_negocio_form = kwargs.pop('p_negocio', None)

        super(IngresoComprasCreateForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['maquina'].queryset = Maquina.objects.filter(negocio=p_negocio_form) 
        self.fields['maquina'].label_from_instance = lambda obj: "%s" % (obj.nombre)
    
    
"""
    IngresoCompras
    -----------------------------------
"""







"""
    InventarioMaquinariaAlquiler
    -----------------------------------
"""
class InventarioMaquinariaAlquilerCreateForm(forms.ModelForm):
    class Meta:
        model = InventarioMaquinariaAlquiler
        fields = '__all__'
        widgets = {
            'maquina': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'precio_por_dia': forms.NumberInput(attrs={'class': 'form-control'}),

            'fecha_baja': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            
            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
    
    
    def __init__(self, *args, **kwargs):
        p_negocio_form = kwargs.pop('p_negocio', None)

        super(InventarioMaquinariaAlquilerCreateForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['maquina'].queryset = Maquina.objects.filter(negocio=p_negocio_form) 
        self.fields['maquina'].label_from_instance = lambda obj: "%s" % (obj.nombre)
    
    
"""
    InventarioMaquinariaAlquiler
    -----------------------------------
"""






"""
    AlquilerMaquina
    -----------------------------------
"""
class AlquilerMaquinaCreateForm(forms.ModelForm):
    class Meta:
        model = AlquilerMaquina
        fields = '__all__'
        widgets = {
            'maquina_alquiler': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'fecha_entrega': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'fecha_devolucion': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),

            'estado_alquiler': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            'observacion_entrega' : forms.TextInput(attrs={'placeholder': ''}),
            'observacion_devolucion' : forms.TextInput(attrs={'placeholder': ''}),

            'anotaciones_seguimiento': forms.Textarea(attrs={"rows":"3"}),

            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
    
    
    def __init__(self, *args, **kwargs):
        p_negocio_form = kwargs.pop('p_negocio', None)

        super(AlquilerMaquinaCreateForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['maquina_alquiler'].queryset = InventarioMaquinariaAlquiler.objects.filter(negocio=p_negocio_form)
        self.fields['maquina_alquiler'].label_from_instance = lambda obj: "%s" % (obj.maquina.nombre)
    
    
"""
    AlquilerMaquina
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
    DetalleFactura
"""
class DetalleFacturaForm(forms.ModelForm):
    class Meta:
        model = DetalleFactura
        fields = '__all__'
        widgets = {
            'maquina_nueva': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'ficha_alquiler': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'cantidad' : forms.TextInput(attrs={'placeholder': ''}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            
            'factura': forms.HiddenInput(),
            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            
        }
    
    
    def __init__(self, p_negocio=None, *args, **kwargs):
        # Asignar el valor de p_negocio a p_obj_negocio
        p_obj_negocio = p_negocio
        # Si está vació 
        if(p_obj_negocio is None):
            # Intenta asignar el valor asignado al kwargs el cual también puede venir nulo
            p_obj_negocio = kwargs.pop('p_negocio', None)

        super(DetalleFacturaForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['maquina_nueva'].queryset = InventarioMaquinariaVentas.objects.filter(negocio=p_obj_negocio, stock__gte = 1)
        self.fields['maquina_nueva'].label_from_instance = lambda obj: "%s" % (obj.maquina.nombre)

        self.fields['ficha_alquiler'].queryset = AlquilerMaquina.objects.filter(negocio=p_obj_negocio, estado_alquiler=1)
        self.fields['ficha_alquiler'].label_from_instance = lambda obj: "%s" % (obj.maquina_alquiler.maquina.nombre)

        
    

"""
    ./DetalleFactura
"""
