from django import forms

from django.forms import ModelForm
from django.contrib.auth.models import User
from apps.plantas.models import Medidas, Producto, DetalleFactura, Inventario, IngresoCompras
from apps.proveedores.models import Proveedor
from apps.factura.models import Factura
from apps.clientes.models import Cliente


"""
    Proveedores
"""
class ProveedorForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'nombre_proveedor' : forms.TextInput(attrs={'placeholder': 'Nombre Proveedor'}),
            'nombre_contacto' : forms.TextInput(attrs={'placeholder': 'Nombre Contacto'}),
            'telefono' : forms.TextInput(attrs={'placeholder': '22224444'}),
            'nit' : forms.TextInput(attrs={'placeholder': 'Número de Nit'}),
            'direccion': forms.Textarea(attrs={"rows":"3"}),

            'negocio': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
    

class ProveedorUpdateForm(forms.ModelForm):
    class Meta:
        model = Proveedor
        fields = '__all__'
        widgets = {
            'nombre_proveedor' : forms.TextInput(attrs={'placeholder': 'Nombre Proveedor'}),
            'nombre_contacto' : forms.TextInput(attrs={'placeholder': 'Nombre Contacto'}),
            'telefono' : forms.TextInput(attrs={'placeholder': '22224444'}),
            'nit' : forms.TextInput(attrs={'placeholder': 'Número de Nit'}),
            'direccion': forms.Textarea(attrs={"rows":"3"}),

            'negocio': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
    

"""
   ./ Proveedores
"""




"""
    Medidas
"""
class MedidasForm(forms.ModelForm):
    class Meta:
        model = Medidas
        fields = '__all__'
        widgets = {
            'medida' : forms.TextInput(attrs={'placeholder': 'Medida'}),
        }
    

class MedidasUpdateForm(forms.ModelForm):
    class Meta:
        model = Medidas
        fields = '__all__'
        widgets = {
            'medida' : forms.TextInput(attrs={'placeholder': 'Medida'}),
            
        }
    

"""
   ./ Medidas
"""




"""
    Producto
"""
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'nombre' : forms.TextInput(attrs={'placeholder': 'Nombre Producto'}),
            'descripcion' : forms.TextInput(attrs={'placeholder': 'Descripción'}),
            'proveedor': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            
        }
    
    def __init__(self, *args, **kwargs):
        p_negocio = kwargs.pop('p_negocio', None) 
        super(ProductoForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['proveedor'].queryset = Proveedor.objects.filter(negocio=p_negocio) 
        self.fields['proveedor'].label_from_instance = lambda obj: "%s" % (obj.nombre_proveedor)

    

class ProductoUpdateForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'nombre' : forms.TextInput(attrs={'placeholder': 'Nombre Producto'}),
            'descripcion' : forms.TextInput(attrs={'placeholder': 'Descripción'}),
            'proveedor': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            
        }
    

"""
   ./ Producto
"""






"""
    Inventario
"""
class InventarioForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = '__all__'
        widgets = {
            'producto': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock' : forms.TextInput(attrs={'placeholder': 'Stock'}),
            'unidad_medida': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            
        }
    
    def __init__(self, *args, **kwargs):
        p_negocio = kwargs.pop('p_negocio', None) 
        super(InventarioForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['producto'].queryset = Producto.objects.filter(negocio=p_negocio) 
        self.fields['producto'].label_from_instance = lambda obj: "%s" % (obj.nombre)

        self.fields['unidad_medida'].label_from_instance = lambda obj: "%s" % (obj.medida)

    

class InventarioUpdateForm(forms.ModelForm):
    class Meta:
        model = Inventario
        fields = '__all__'
        widgets = {
            #'producto': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0.00'}),
            'stock' : forms.TextInput(attrs={'placeholder': 'Stock'}),
            'unidad_medida': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            'producto': forms.HiddenInput(),
            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            
        }
    def __init__(self, *args, **kwargs):
        super(InventarioUpdateForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['unidad_medida'].label_from_instance = lambda obj: "%s" % (obj.medida)
    

"""
   ./ Inventario
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
            'producto': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'precio': forms.NumberInput(attrs={'class': 'form-control'}),
            'precio_compra': forms.NumberInput(attrs={'class': 'form-control'}),
            'cantidad': forms.NumberInput(attrs={'class': 'form-control'}),
            'unidad_medida': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            
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
        self.fields['producto'].queryset = Producto.objects.filter(negocio=p_negocio_form) 
        self.fields['producto'].label_from_instance = lambda obj: "%s" % (obj.nombre)
    
    
"""
    IngresoCompras
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
            'producto': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
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
        self.fields['producto'].queryset = Producto.objects.filter(negocio=p_obj_negocio, relInventarioProducto__stock__gte = 1)
        self.fields['producto'].label_from_instance = lambda obj: "%s" % (obj.nombre)


"""
    ./DetalleFactura
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
FILTROS PARA EL CONSUMO REST
=================================================
"""

"""
    Inventario
"""
class InventarioRestForm(forms.Form):
    """Formulario que Controla los filtros para poder hacer busquedas
    """
    producto = forms.ModelChoiceField(
        queryset=Producto.objects.all(),
        label='Producto',
        required=False,
        widget=forms.Select(attrs={'class': 'form-select form-select-sm select2bs4'}))

    stock = forms.CharField(
        label='Stock',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control form-control-sm'}))
    
    
    def __init__(self, *args, **kwargs):
        p_negocio = kwargs.pop('p_negocio', None) 

        super(InventarioRestForm, self).__init__(*args, **kwargs)
        self.fields['producto'].queryset = Producto.objects.filter(negocio=p_negocio) 
        self.fields['producto'].label_from_instance = lambda obj: "%s" % (obj.nombre)
        
        