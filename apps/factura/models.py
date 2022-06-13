from multiprocessing.connection import Client
from django.db import models

from django.contrib.auth.models import User
from django.utils import timezone #Agregada por mi para el manejo de la fecha
from decimal import Decimal
from datetime import datetime

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete

from apps.registration.models import Negocio
from apps.clientes.models import Cliente, NegocioCliente


class ControlCreaciones(models.Model):
    """
    La clase ControlCreaciones es una clase abstracta que contiene
    campos comúnes que se ocupan en varias clases.

    Attributes:
        creado : DateTimeField
            Fecha y hora de creación.
        actualizado : DateTimeField
            Fecha y hora de modificación.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    creado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    actualizado = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")

    class Meta:
        abstract = True





class EstadoFactura(models.Model):
    """
    La clase EstadoFactura se utiliza para almacenar la lista de los estados para las facturas.
    Ejemplo: En edición, Lista para entregar, Anulada y Entregada.

    Attributes:
        nombre_estado : CharField
            Nombre del estado de la factura.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    nombre_estado = models.CharField(max_length=150, blank=True, null=True, verbose_name="Estado de Factura")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el estado de la factura.
        """
        return '({}) {}'.format(self.id, self.nombre_estado)

    class Meta:
        verbose_name='Estado de la Factura'
        verbose_name_plural='Estados de la Factura'
        ordering = ['-id']


class TipoPago(models.Model):
    """
    La clase TipoPago se utiliza para almacenar los tipos de pago recibidos.
    Ejemplo: Efectivo, Cheque, Transferencia, Depósito en Banco, etc.

    Attributes:
        nombre_tipo_pago : CharField
            Nombre del tipo de pago recibido.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    nombre_tipo_pago = models.CharField(max_length=150, blank=True, null=True, verbose_name="Tipo de Pago")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el tipo de pago recibido.
        """
        return '({}) {}'.format(self.id, self.nombre_tipo_pago)
    
    class Meta:
        verbose_name='Tipo de Pago'
        verbose_name_plural='Tipos de Pago'
        ordering = ['-id']


class EstadoVenta(models.Model):
    """
    La clase EstadoVenta se utiliza para almacenar el estado de la venta.
    Ejemplo: Pendiente de pago, Anulada, Completada.

    Attributes:
        nombre_estado_venta : CharField
            Nombre del estado de la Venta.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    nombre_estado_venta = models.CharField(max_length=150, blank=True, null=True, verbose_name="Estado de la Venta")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el estado de la venta.
        """
        return '({}) {}'.format(self.id, self.nombre_estado_venta)
    
    class Meta:
        verbose_name='Estado de la Venta'
        verbose_name_plural='Estado de las Ventas'
        ordering = ['-id']



class CorrelativoFactura(ControlCreaciones):
    """
    La clase CorrelativoFactura se utiliza para almacenar un número correlativo de factura para cada Negocio.
    
    Attributes:
        correlativo : IntegerField
            Lleva el contador o correlativo de facturas emitidas por Negocio.
        nomenclatura : CharField
            Nombre del estado de la Venta.
        negocio : ForeignKey
            Relación muchos a uno, CorrelativoFactura con el Negocio.

    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    correlativo = models.IntegerField(blank=False, null=False, verbose_name="Correlativo Factura")
    nomenclatura = models.CharField(max_length=15, blank=False, null=False, verbose_name="Nomenclatura Negocio")
    negocio = models.ForeignKey(Negocio, related_name='relCorrelativoFacturaNegocio', on_delete=models.CASCADE, null=False, blank=False, verbose_name="Negocio")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id, nomenclatura y correlativo.
        """
        return '({}) {}-{}'.format(self.id, self.nomenclatura, self.correlativo)

    class Meta:
        unique_together = (("correlativo", "nomenclatura", "negocio"),)
        verbose_name='Correlativo de Factura'
        verbose_name_plural='Correlativos de Facturas'
        ordering = ['-id']




class EstadoPedido(models.Model):
    """
    La clase EstadoPedido se utiliza para almacenar la lista de los estados para los pedidos de los clientes.
    Ejemplo: Nueva Solicitud, Solicitud con vendedor, Anulado, Completado

    Attributes:
        nombre_estado : CharField
            Nombre del estado del Pedido.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    nombre_estado = models.CharField(max_length=150, blank=True, null=True, verbose_name="Estado del Pedido")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el estado del pedido.
        """
        return '({}) {}'.format(self.id, self.nombre_estado)

    class Meta:
        verbose_name='Estado del Pedido'
        verbose_name_plural='Estados de los Pedidos'
        ordering = ['-id']




class Pedido(ControlCreaciones):
    """
    La clase Pedido se utiliza para almacenar los Pedido creados por los Clientes.
    El cliente no genera un detalle factura en línea, con esta clase Pedido realiza una solicitud
    del detalle de su requerimiento la cual será atendida por el vendedor asignado al cliente.
    
    Attributes:
        cliente : ForeignKey
            Relación muchos a uno, Pedido con Cliente.
        fecha_pedido : DateField
            Almacena la fecha en la que se genera el pedido.
        descripcion_detalle_pedido : TextField
            Almacena el detalle de la solicitud en una caja de texto.
        vendedor : ForeignKey
            Relación muchos a uno, Pedido con el Usuario vendedor.
        estado_pedido : ForeignKey
            Relación muchos a uno, Pedido con el estado del mismo Pedido.
        anotaciones_seguimiento : TextField
            Permite al vendedor hacer anotaciones sobre el pedido del cliente.
            El cliente podrá ver estas anotaciones más no podrá modificarlas.
        completado : BooleanField
            Bandera, indicador de Pedido Completada.
        negocio : ForeignKey
            Relación muchos a uno, Pedido con el Negocio.
        
    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    cliente = models.ForeignKey(Cliente, related_name='relPedidoCliente', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Cliente")
    negocio = models.ForeignKey(Negocio, related_name='relPedidoNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Categoría de Negocio")
    fecha_pedido = models.DateField(null=True, blank=True, verbose_name="Fecha de Pedido")
    descripcion_detalle_pedido = models.TextField(blank=True, null=True, verbose_name="Detalle del Pedido")
    vendedor = models.ForeignKey(User, related_name='relPedidoUserVendedor', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Vendedor Asignado")
    estado_pedido = models.ForeignKey(EstadoPedido, related_name='relPedidoEstadoPedido', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Estado del Pedido")
    anotaciones_seguimiento = models.TextField(blank=True, null=True, verbose_name="Anotaciones de Seguimiento")
    completado = models.BooleanField(default=False)
    

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id, cliente, fecha pedido.
        """
        return '({}) ({}) - {}'.format(self.id, self.cliente, self.fecha_pedido)

    class Meta:
        verbose_name='Pedido'
        verbose_name_plural='Pedidos'
        ordering = ['-id']


"""
    Función signal para obtener el vendedor asignado a un cliente para un giro de negocio en específico
"""
@receiver(pre_save, sender=Pedido) 
def fn_asignar_vendedor(sender, instance, **kwargs):

    # VALIDA SI SE CREO
    if kwargs.get('created', True):
        if(instance.negocio and instance.cliente):
            ObjVendedor = NegocioCliente.objects.get(negocio=instance.negocio, cliente=instance.cliente)
            instance.vendedor = ObjVendedor.vendedor





class Factura(ControlCreaciones):
    """
    La clase Factura se utiliza para almacenar las facturas emitidas por Negocio.
    
    Attributes:
        numero_factura : IntegerField
            Lleva el contador o correlativo de facturas emitidas por Negocio.
        cliente : ForeignKey
            Relación muchos a uno, Factura con Cliente.
        fecha_factura : DateField
            Almacena la fecha en la que se emite la factura.
        monto_total : DecimalField
            Almacena el total calculado de la factura.
        vendedor : ForeignKey
            Relación muchos a uno, Factura con el Usuario vendedor.
        estado_factura : ForeignKey
            Relación muchos a uno, Factura con el estado de la factura.
        tipo_pago : ForeignKey
            Relación muchos a uno, Factura con el tipo de pago.
        estado_venta : ForeignKey
            Relación muchos a uno, Factura con el estado de la Venta.
        completada : BooleanField
            Bandera, indicador de Factura Completada.
        negocio : ForeignKey
            Relación muchos a uno, Factura con el Negocio.
        creado_por : ForeignKey
            Relación muchos a uno, Factura con el usuario que creó la factura.
        actualizado_por : ForeignKey
            Relación muchos a uno, Factura con el usuario que modificó la factura.

    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    numero_factura = models.IntegerField(blank=True, null=True, verbose_name="Número Factura")
    cliente = models.ForeignKey(Cliente, related_name='relFacturaCliente', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Cliente")
    pedido = models.ForeignKey(Pedido, related_name='relFacturaPedido', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Pedido")
    fecha_factura = models.DateField(null=True, blank=True, verbose_name="Fecha de la Factura")
    monto_total = models.DecimalField(max_digits=13, default=0.00, decimal_places=2, null=True, blank=True, verbose_name="Monto Facturado")
    vendedor = models.ForeignKey(User, related_name='relFacturaUserVendedor', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Vendedor Asignado")
    estado_factura = models.ForeignKey(EstadoFactura, related_name='relFacturaEstadoFactura', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Estado Factura")
    tipo_pago = models.ForeignKey(TipoPago, related_name='relFacturaTipoPago', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Tipo de Pago")
    estado_venta = models.ForeignKey(EstadoVenta, related_name='relFacturaEstadoVenta', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Estado de la Venta")
    completada = models.BooleanField(default=False)
    negocio = models.ForeignKey(Negocio, related_name='relFacturaNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")
    
    creado_por = models.ForeignKey(User, related_name='relFacturaCreateUser', on_delete=models.CASCADE, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, related_name='relFacturaUpdateUser', on_delete=models.CASCADE, null=True, blank=True)

    def fn_valida_cierre(self):

        if (self.completada and self.estado_factura.id == 4 and self.estado_venta.id == 3):
            return True
        else:
            return False

    
    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id, número de factura, fecha y monto.
        """
        return '({}) ({}) - {} - {}'.format(self.id, self.numero_factura, self.fecha_factura, self.monto_total)

    class Meta:
        unique_together = (("numero_factura", "negocio"),)
        verbose_name='Factura'
        verbose_name_plural='Facturas'
        ordering = ['-id']



@receiver(pre_save, sender=Factura) 
def fn_calcular_numero_factura(sender, instance, **kwargs):

    #print(instance.relPlantasDetalleFacturaFactura.all())
    #print(instance.relPlantasDetalleFacturaFactura.count())

    if(instance.fn_valida_cierre):
    
        # Guarda el total del detalle de la factura desde PLANTAS.
        if(instance.relPlantasDetalleFacturaFactura.count() > 0):
            Total = sum(detalle.fn_subtotal() for detalle in instance.relPlantasDetalleFacturaFactura.all())
            instance.monto_total = Total
            

        # Guarda el total del detalle de la factura desde PROYECTOS.
        if(instance.relFacturaProyecto.count() > 0):
            Total = sum(detalle.monto for detalle in instance.relFacturaProyecto.all())
            instance.monto_total = Total
        

        # Guarda el total del detalle de la factura desde TRANSPORTES.
        if(instance.relRutasFactura.count() > 0):
            Total = sum(detalle.fn_calcular_monto_facturar() for detalle in instance.relRutasFactura.all())
            instance.monto_total = Total
        

        # Guarda el total del detalle de la factura desde MAQUINAS.
        if(instance.relDetalleFacturaVAMaquinariaFactura.count() > 0):
            Total = sum(detalle.fn_subtotal() for detalle in instance.relDetalleFacturaVAMaquinariaFactura.all())
            instance.monto_total = Total
        

    
    # VALIDA SI SE CREO
    if kwargs.get('created', True):
        # Entra si tiene número de recibo
        if(instance.numero_factura is None):
            ObjNumeroFactura = CorrelativoFactura.objects.get(negocio=instance.negocio) # contador facturas
            
            lv_numero_factura = ObjNumeroFactura.correlativo + 1 # Al último número registrado, sumarle 1.
            instance.numero_factura = lv_numero_factura
            
            # Actualizar el nuevo correlativo en la tabla de control
            ObjNumeroFactura.correlativo = lv_numero_factura
            ObjNumeroFactura.save()




@receiver(post_save, sender=Factura) 
def fn_pasar_monto_total_ventas(sender, instance, **kwargs):
    
    # Completada = True
    # estado_factura = 4 Completado
    # estado_venta = 3 Completado
    if (instance.completada and instance.estado_factura.id == 4 and instance.estado_venta.id == 3):
        try:

            if(instance.pedido):
                ObjPedido = Pedido.objects.get(id=instance.pedido.id)
                ObjPedido.estado_pedido.id = 4 # 4=completado
                ObjPedido.completado = True
                ObjPedido.save()
            
            print("+++++++++++++")


            # Instanciar el objeto Ventas
            ObjVentas = Ventas.objects.filter(factura=instance).count()

            # No se permite el registro de facturas duplicadas para el mismo negocio.
            if(ObjVentas==0):
                Ventas.objects.create(  factura = instance, 
                                fecha_registro=instance.fecha_factura, 
                                monto_venta = instance.monto_total, 
                                negocio = instance.negocio, 
                                creado_por = instance.creado_por
                                )
        except Exception as e:
            print('Error: ' + str(e))
            




class Ventas(ControlCreaciones):
    """
    La clase Ventas se utiliza para almacenar las Ventas facturadas por Negocio.
    
    Attributes:
        factura : ForeignKey
            Relación muchos a uno, Venta con la Factura.
        fecha_registro : DateField
            Almacena la fecha en la que confirmó e hizo registro de la Venta.
        monto_venta : DecimalField
            Almacena el monto de la Venta.
        negocio : ForeignKey
            Relación muchos a uno, Ventas con Negocio.
        creado_por : ForeignKey
            Relación muchos a uno, Ventas con Usuario que Creó.
        actualizado_por : ForeignKey
            Relación muchos a uno, Ventas con Usuario que Actualizó.

    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    factura = models.ForeignKey(Factura, related_name='relVentasFactura', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Factura")
    fecha_registro = models.DateField(null=False, blank=False, verbose_name="Fecha de Registro")
    monto_venta = models.DecimalField(max_digits=15, decimal_places=2, null=False, blank=False, verbose_name="Monto Venta")
    negocio = models.ForeignKey(Negocio, related_name='relVentasNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")
    
    creado_por = models.ForeignKey(User, related_name='relVentasCreateUser', on_delete=models.CASCADE, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, related_name='relVentasUpdateUser', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id, número de factura, fecha y monto.
        """
        return '({}) ({}) - {} - {}'.format(self.id, self.factura.numero_factura, self.fecha_registro, self.monto_venta)

    class Meta:
        unique_together = (("factura", "negocio"),)
        verbose_name='Venta'
        verbose_name_plural='Ventas'
        ordering = ['-id']






class EstadoDespacho(models.Model):
    """
    La clase EstadoDespacho se utiliza para almacenar la lista de los estados del Despacho de las solicitudes del Cliente.

    Attributes:
        nombre_estado : CharField
            Nombre del estado del despacho.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    nombre_estado = models.CharField(max_length=150, blank=True, null=True, verbose_name="Estado del Despacho")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el estado del despacho.
        """
        return '({}) {}'.format(self.id, self.nombre_estado)

    class Meta:
        verbose_name='Estado del Despacho'
        verbose_name_plural='Estados de los Despachos'
        ordering = ['-id']




class Despacho(ControlCreaciones):
    """
    La clase Despacho se utiliza para almacenar los Despacho de las solicitudes de los Clientes.
    
    Attributes:
        factura : ForeignKey
            Relación muchos a uno, Despacho con Factura.
        fecha_despacho : DateField
            Almacena la fecha en la que se genera el Despacho.
        persona_recibe : CharField
            Almacena la persona que recibe el producto a entregar por el empleado asignado.
        empleado : ForeignKey
            Relación muchos a uno, Despacho con el Empleado que entrega el producto.
        anotaciones_despacho : TextField
            Permite al empleado realizar anotaciones u observaciones acerca del despacho.
            El cliente podrá ver estas anotaciones más no podrá modificarlas.
        estado_despacho : ForeignKey
            Relación muchos a uno, Despacho con sus Estados.
        completado : BooleanField
            Bandera, indicador de Pedido Completada.
        negocio : ForeignKey
            Relación muchos a uno, Despacho con el Negocio.
        creado_por : ForeignKey
            Relación muchos a uno, Despacho con Usuario que Creó.
        actualizado_por : ForeignKey
            Relación muchos a uno, Despacho con Usuario que Actualizó.

    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    factura = models.ForeignKey(Factura, related_name='relDespachoFactura', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Factura")
    fecha_despacho = models.DateField(null=False, blank=False, verbose_name="Fecha del Despacho")
    persona_recibe = models.CharField(max_length=150, blank=True, null=True, verbose_name="Persona que Recibe")
    empleado = models.ForeignKey(User, related_name='relDespachoUserEmpleado', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Empleado Entrega")
    anotaciones_despacho = models.TextField(blank=True, null=True, verbose_name="Anotaciones del Despacho")
    estado_despacho = models.ForeignKey(EstadoDespacho, related_name='relDespachoEstadoDespacho', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Estado del Despacho")
    completado = models.BooleanField(default=False)
    
    negocio = models.ForeignKey(Negocio, related_name='relDespachoNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    creado_por = models.ForeignKey(User, related_name='relDespachoCreateUser', on_delete=models.CASCADE, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, related_name='relDespachoUpdateUser', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id, factura, fecha despacho.
        """
        return '({}) ({}) - {}'.format(self.id, self.factura, self.fecha_despacho)

    class Meta:
        verbose_name='Despacho'
        verbose_name_plural='Despachos'
        ordering = ['-id']


