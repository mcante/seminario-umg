from django import forms

from django.forms import ModelForm
from django.contrib.auth.models import User
from apps.registration.models import Negocio, Perfil

from .models import Marca, Linea, TipoVehiculo, TransmisionVehiculo, \
DispositivoGPS, InventarioVehiculo, AsignacionTarifa, \
Rutas, TipoLog, LogRuta, FichaSalida, FichaEntrada

from apps.proveedores.models import Proveedor
from apps.factura.models import Factura, Pedido
from apps.clientes.models import Cliente





"""
    DispositivoGPS
"""
class DispositivoGPSForm(forms.ModelForm):
    class Meta:
        model = DispositivoGPS
        fields = '__all__'
        widgets = {
            'identificador' : forms.TextInput(attrs={'placeholder': ''}),
            #'activo' : forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

"""
   ./ DispositivoGPS
"""





"""
    InventarioVehiculo
    -----------------------------------
"""
class InventarioVehiculoCreateForm(forms.ModelForm):
    class Meta:
        model = InventarioVehiculo
        fields = '__all__'
        widgets = {
            'fecha_ingreso': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),

            'marca': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'linea': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'modelo' : forms.TextInput(attrs={'placeholder': ''}),
            'tipo_vehiculo': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'tipo_transmision': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            'color' : forms.TextInput(attrs={'placeholder': ''}),
            'cilindraje' : forms.TextInput(attrs={'placeholder': ''}),
            'numero_chasis' : forms.TextInput(attrs={'placeholder': ''}),
            'tonelaje' : forms.TextInput(attrs={'placeholder': ''}),
            'planca' : forms.TextInput(attrs={'placeholder': ''}),

            #'disponible' : forms.CheckboxInput(attrs={'class': 'form-check-input form-control-sm'}),
            #'permiso_fronterizo' : forms.CheckboxInput(attrs={'class': 'form-check-input form-control-sm'}),

            'dispositivo_gps': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            #'baja' : forms.CheckboxInput(attrs={'class': 'form-check-input form-control-sm'}),
            'fecha_baja': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),


            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }
    
    
"""
    InventarioVehiculo
    -----------------------------------
"""






"""
    AsignacionTarifa
    -----------------------------------
"""
class AsignacionTarifaCreateForm(forms.ModelForm):
    class Meta:
        model = AsignacionTarifa
        fields = '__all__'
        widgets = {
            #'vehiculo': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'fecha_autorizacion': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'precio_por_kilometro': forms.NumberInput(attrs={'class': 'form-control-sm'}),
            
            'vehiculo': forms.HiddenInput(),
        }
    
    
"""
    AsignacionTarifa
    -----------------------------------
"""




"""
    Rutas
    -----------------------------------
"""
class RutasCreateForm(forms.ModelForm):
    class Meta:
        model = Rutas
        fields = '__all__'
        widgets = {
            #'factura': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'vehiculo': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'piloto': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            
            'fecha_salida_predio': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'fecha_entrada_predio': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),

            'kilometraje_salida' : forms.TextInput(attrs={'placeholder': ''}),
            'kilometraje_entrada' : forms.TextInput(attrs={'placeholder': ''}),
            'kilometros_recorridos' : forms.TextInput(attrs={'placeholder': ''}),

            'direccion_recoleccion': forms.Textarea(attrs={"rows":"3"}),
            'contacto_recoleccion': forms.Textarea(attrs={"rows":"3"}),
            'fecha_hora_recoleccion': forms.DateTimeInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),

            'direccion_entrega': forms.Textarea(attrs={"rows":"3"}),
            'fecha_hora_entrega': forms.DateTimeInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'contacto_entrega': forms.Textarea(attrs={"rows":"3"}),
            
            #'es_nacional' : forms.CheckboxInput(attrs={'class': 'form-check-input form-control-sm'}),

            'factura': forms.HiddenInput(),
            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }

    def __init__(self, p_negocio = None, *args, **kwargs):
        p_negocio_form = kwargs.pop('p_negocio', None)

        # Obtener variable del formulario de Rutas o la variable del subformulario de Facturas
        lv_negocio = None
        if p_negocio_form:
            lv_negocio = p_negocio_form
        elif p_negocio:
            lv_negocio = p_negocio

        super(RutasCreateForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['vehiculo'].queryset = InventarioVehiculo.objects.filter(negocio=lv_negocio) # tipo_empleado = 1 = VENDEDOR
        self.fields['vehiculo'].label_from_instance = lambda obj: "%s - %s (%s)" % (obj.marca, obj.placa, obj.tipo_vehiculo.tipo_vehiculo)

        self.fields['piloto'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=4, relPerfilUsuario__negocio=lv_negocio)
        self.fields['piloto'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())





class RutasLogPilotoUpdateForm(forms.ModelForm):
    class Meta:
        model = Rutas
        fields = '__all__'
        widgets = {
            #'factura': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            #'vehiculo': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            #'piloto': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            
            #'fecha_salida_predio': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'fecha_entrada_predio': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),

            #'kilometraje_salida' : forms.TextInput(attrs={'placeholder': ''}),
            'kilometraje_entrada' : forms.TextInput(attrs={'placeholder': ''}),
            #'kilometros_recorridos' : forms.TextInput(attrs={'placeholder': ''}),

            'direccion_recoleccion': forms.Textarea(attrs={"rows":"3"}),
            'contacto_recoleccion': forms.Textarea(attrs={"rows":"3"}),
            'fecha_hora_recoleccion': forms.DateTimeInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),

            'direccion_entrega': forms.Textarea(attrs={"rows":"3"}),
            'fecha_hora_entrega': forms.DateTimeInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'contacto_entrega': forms.Textarea(attrs={"rows":"3"}),
            
            #'es_nacional' : forms.CheckboxInput(attrs={'class': 'form-check-input form-control-sm'}),

            'vehiculo': forms.HiddenInput(),
            'piloto': forms.HiddenInput(),
            'fecha_salida_predio': forms.HiddenInput(),

            'kilometraje_salida': forms.HiddenInput(),
            'kilometros_recorridos': forms.HiddenInput(),
            

            
            'factura': forms.HiddenInput(),
            'es_nacional': forms.HiddenInput(),
            'completada': forms.HiddenInput(),
            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }

    
"""
    Rutas
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
            #'pedido': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'fecha_factura': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'vendedor': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            'estado_factura': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'tipo_pago': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'estado_venta': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            'numero_factura': forms.HiddenInput(),
            'pedido': forms.HiddenInput(),
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
            self.fields['pedido'].label_from_instance = lambda obj: "%s" % (obj.nombre_empresa)
        else:
            self.fields['cliente'].queryset = Cliente.objects.all()
            self.fields['cliente'].label_from_instance = lambda obj: "%s" % (obj.nombre_empresa)
    


class FacturaUpdateForm(forms.ModelForm):
    class Meta:
        model = Factura
        fields = '__all__'
        widgets = {
            'cliente': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            #'pedido': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'fecha_factura': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'monto_total': forms.NumberInput(attrs={'class': 'form-control'}),
            'vendedor': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            'estado_factura': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'tipo_pago': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'estado_venta': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),

            'numero_factura': forms.HiddenInput(),
            'pedido': forms.HiddenInput(),
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
    FichaSalida
    -----------------------------------
"""
class FichaSalidaCreateForm(forms.ModelForm):
    class Meta:
        model = FichaSalida
        fields = '__all__'
        widgets = {
            #'ruta': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'quien_entrega': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'piloto': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            
            'fecha_revision': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'kilometraje' : forms.TextInput(attrs={'placeholder': ''}),

            'observacion_llantas': forms.Textarea(attrs={"rows":"3"}),
            'observacion_tapiceria': forms.Textarea(attrs={"rows":"3"}),
            'observacion_carroceria': forms.Textarea(attrs={"rows":"3"}),
            'observacion_combustible': forms.Textarea(attrs={"rows":"3"}),

            'ruta': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }

    
    def __init__(self, p_negocio=None, *args, **kwargs):
        p_negocio_form = kwargs.pop('p_negocio', None)

        # Obtener variable del formulario de FichaSalida o la variable del subformulario de Facturas
        lv_negocio = None
        if p_negocio_form:
            lv_negocio = p_negocio_form
        elif p_negocio:
            lv_negocio = p_negocio
        
        #print(lv_negocio)

        super(FichaSalidaCreateForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['quien_entrega'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=1, relPerfilUsuario__negocio=lv_negocio)
        self.fields['quien_entrega'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())

        self.fields['piloto'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=4, relPerfilUsuario__negocio=lv_negocio)
        self.fields['piloto'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())
    
    
"""
    FichaSalida
    -----------------------------------
"""




"""
    FichaEntrada
    -----------------------------------
"""
class FichaEntradaCreateForm(forms.ModelForm):
    class Meta:
        model = FichaEntrada
        fields = '__all__'
        widgets = {
            #'ruta': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'piloto_entrega': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            'quien_recibe': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            
            'fecha_revision': forms.DateInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'kilometraje' : forms.TextInput(attrs={'placeholder': ''}),

            'observacion_llantas': forms.Textarea(attrs={"rows":"3"}),
            'observacion_tapiceria': forms.Textarea(attrs={"rows":"3"}),
            'observacion_carroceria': forms.Textarea(attrs={"rows":"3"}),
            'observacion_combustible': forms.Textarea(attrs={"rows":"3"}),
            'observacion_general': forms.Textarea(attrs={"rows":"3"}),

            'ruta': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }

    
    def __init__(self, p_negocio=None, *args, **kwargs):
        p_negocio_form = kwargs.pop('p_negocio', None)

        # Obtener variable del formulario de FichaEntrada o la variable del subformulario de Facturas
        lv_negocio = None
        if p_negocio_form:
            lv_negocio = p_negocio_form
        elif p_negocio:
            lv_negocio = p_negocio

        super(FichaEntradaCreateForm, self).__init__(*args, **kwargs)

        # queryset: Cambia el QuerySet por la consulta personalizada.
        # label_from_instance: Cambia la etiqueta que se virualiza en el select
        self.fields['quien_recibe'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=1, relPerfilUsuario__negocio=lv_negocio)
        self.fields['quien_recibe'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())

        self.fields['piloto_entrega'].queryset = User.objects.filter(relPerfilUsuario__activo=True, relPerfilUsuario__tipo_empleado=4, relPerfilUsuario__negocio=lv_negocio)
        self.fields['piloto_entrega'].label_from_instance = lambda obj: "%s" % (obj.get_full_name())
    
    
"""
    FichaEntrada
    -----------------------------------
"""





"""
    LogRuta
    -----------------------------------
"""
class LogRutaCreateForm(forms.ModelForm):
    class Meta:
        model = LogRuta
        fields = '__all__'
        widgets = {
            'tipo_log': forms.Select(attrs={'class': 'select2bs4 form-control-sm', 'style':'width: 100%;'}),
            #'fecha_hora_log': forms.DateTimeInput(attrs={'class': 'datepicker', 'placeholder': 'dd/mm/aaaa'}),
            'observaciones': forms.Textarea(attrs={"rows":"3"}),

            'ruta': forms.HiddenInput(),
            'fecha_hora_log': forms.HiddenInput(),
            'negocio': forms.HiddenInput(),
            'creado_por': forms.HiddenInput(),
            'actualizado_por': forms.HiddenInput(),
            'creado': forms.HiddenInput(),
            'actualizado': forms.HiddenInput(),
            
        }

    
"""
    ./LogRuta
    -----------------------------------
"""
