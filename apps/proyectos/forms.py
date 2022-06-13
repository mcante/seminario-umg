from django import forms

from django.forms import ModelForm
from django.contrib.auth.models import User
from apps.registration.models import Negocio, Perfil
from .models import TipoProyecto, Proyecto, Documentos, GastosProyecto, DetalleFacturaEntregables
from apps.proveedores.models import Proveedor
from apps.factura.models import Factura, Pedido
from apps.clientes.models import Cliente





"""
    Proyectos
"""
class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = '__all__'
        widgets = {
            'cliente': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'nombre_proyecto' : forms.TextInput(attrs={'placeholder': ''}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'tipo_proyecto': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'descripcion': forms.Textarea(attrs={"rows":"3"}),
            'presupuesto_estimado': forms.NumberInput(attrs={'class': 'form-control'}),
            'gastos_totales': forms.NumberInput(attrs={'class': 'form-control'}),
            'empleado': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            #'completado' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'completado': forms.HiddenInput(),
            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }

    def __init__(self, *args, **kwargs):
        p_negocio = kwargs.pop('p_negocio', None) # Aun no implementado para validar la lista de vendedores asociados con el cliente.

        super(ProyectoForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['empleado'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=1, relPerfilUsuario__negocio=p_negocio) # tipo_empleado = 1 = VENDEDOR
        self.fields['empleado'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())

        if(p_negocio):
            self.fields['cliente'].queryset = Cliente.objects.filter(relNegocioClienteCliente__negocio=p_negocio)
            self.fields['cliente'].label_from_instance = lambda obj: "%s" % (obj.nombre_empresa)
        else:
            self.fields['cliente'].queryset = Cliente.objects.all()
            self.fields['cliente'].label_from_instance = lambda obj: "%s" % (obj.nombre_empresa)
    

class ProyectoUpdateForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = '__all__'
        widgets = {
            #'cliente': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'nombre_proyecto' : forms.TextInput(attrs={'placeholder': ''}),
            'fecha_inicio': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'fecha_fin': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'tipo_proyecto': forms.Select(attrs={'class': 'select2bs4', 'style':'width: 100%;'}),
            'descripcion': forms.Textarea(attrs={"rows":"3"}),
            'presupuesto_estimado': forms.NumberInput(attrs={'class': 'form-control'}),
            'gastos_totales': forms.NumberInput(attrs={'class': 'form-control'}),
            'empleado': forms.Select(attrs={'class': 'select2bs4', 'style':'width: 100%;'}),
            'completado' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),

            'cliente': forms.HiddenInput(),
            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
    
    def __init__(self, *args, **kwargs):
        #p_negocio = kwargs.pop('p_negocio', None) # Aun no implementado para validar la lista de vendedores asociados con el cliente.
        super(ProyectoUpdateForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['empleado'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=1) # tipo_empleado = 1 = VENDEDOR
        self.fields['empleado'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())


"""
   ./ Proyectos
"""







"""
    Documentos
"""
class DocumentosForm(forms.ModelForm):
    class Meta:
        model = Documentos
        fields = '__all__'
        widgets = {
            #'proyecto': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'titulo_documento' : forms.TextInput(attrs={'placeholder': ''}),
            'descripcion': forms.Textarea(attrs={"rows":"3"}),

            'proyecto': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
"""
    ./Documentos
"""
    


"""
    GastosProyecto
"""
class GastosProyectoForm(forms.ModelForm):
    class Meta:
        model = GastosProyecto
        fields = '__all__'
        widgets = {
            
            'titulo_gasto' : forms.TextInput(attrs={'placeholder': ''}),
            'descripcion': forms.Textarea(attrs={"rows":"3"}),
            'fecha_gasto': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'autorizado_por': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            
            'proyecto': forms.HiddenInput(),
            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
    
    def __init__(self, *args, **kwargs):
        super(GastosProyectoForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['autorizado_por'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=2) # tipo_empleado = 2 = ADMINISTRATIVO
        self.fields['autorizado_por'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())
"""
    ./GastosProyecto
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
            'fecha_factura': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'vendedor': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            'estado_factura': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'tipo_pago': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'estado_venta': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            'numero_factura': forms.HiddenInput(),
            #'pedido': forms.HiddenInput(),
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

            self.fields['pedido'].queryset = Pedido.objects.filter(negocio=p_negocio)
            self.fields['pedido'].label_from_instance = lambda obj: "%s" % (obj.cliente)
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
            'fecha_factura': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'vendedor': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            'estado_factura': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'tipo_pago': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'estado_venta': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            'numero_factura': forms.HiddenInput(),
            #'pedido': forms.HiddenInput(),
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

            self.fields['pedido'].queryset = Pedido.objects.filter(negocio=p_negocio)
            self.fields['pedido'].label_from_instance = lambda obj: "%s" % (obj.cliente)
        else:
            self.fields['cliente'].queryset = Cliente.objects.all()
            self.fields['cliente'].label_from_instance = lambda obj: "%s" % (obj.nombre_empresa)
    
"""
    FACTURA
    -----------------------------------
"""




"""
    DetalleFacturaEntregables
"""
class DetalleFacturaEntregablesForm(forms.ModelForm):
    class Meta:
        model = DetalleFacturaEntregables
        fields = '__all__'
        widgets = {
            'proyecto': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'fecha_entregable': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'monto': forms.NumberInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={"rows":"3"}),
            
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

        super(DetalleFacturaEntregablesForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['proyecto'].queryset = Proyecto.objects.filter(negocio=p_obj_negocio, completado = False)
        self.fields['proyecto'].label_from_instance = lambda obj: "%s - %s (%s)" % (obj.cliente.nombre_empresa, obj.nombre_proyecto, obj.id)


"""
    ./DetalleFactura
"""