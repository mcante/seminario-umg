from django.db import models
from django.contrib.auth.models import User

from apps.factura.models import Factura
from apps.registration.models import Negocio
from apps.proveedores.models import Proveedor

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete

from django.db.models import Count, F, Value


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



class Marca(models.Model):
    """
    La clase Marca se utiliza para almacenar la lista Marcas de vehículos.

    Attributes:
        nombre : CharField
            Nombre de la Marca.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    nombre = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre Marca")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el nombre de la marca.
        """
        return '({}) {}'.format(self.id, self.nombre)

    class Meta:
        verbose_name='Marca'
        verbose_name_plural='Marcas'
        ordering = ['-id']






class TipoMaquina(models.Model):
    """
    La clase TipoMaquina se utiliza para almacenar la lista de Tipos de Máquinas.

    Attributes:
        nombre : CharField
            Almacena el Nombre de la Tipo de Máquina.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    nombre = models.CharField(max_length=150, blank=True, null=True, verbose_name="Tipo de Máquina")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el nombre de la marca.
        """
        return '({}) {}'.format(self.id, self.nombre)

    class Meta:
        verbose_name='Tipo Máquina'
        verbose_name_plural='Tipos de Máquinas'
        ordering = ['-id']








def elimina_imagen_cargada(instance, filename):
    """
    Función que eliminara físicamente alguna imagen que contenga el mismo nombre que el que se pasa como argumento.

    Args:
        instance (clase Maquina): Instancia de la clase de que invoca.
        filename (str): Nombre de la ruta del archivo físico al que apunta la imagen.

    Returns:
        str: Devuelve la dirección física de la imagen
    """
    try:
        old_instance = Maquina.objects.get(pk=instance.pk)
        old_instance.imagen_maquina.delete()
    except:
        old_instance = None
    return 'maquinas/' + filename

class Maquina(ControlCreaciones):
    """
    La clase Maquina se utiliza para almacenar la lista de Máquinas.

    Attributes:
        marca : ForeignKey
            Relación muchos a uno, Maquina con el Marca.
        proveedor : ForeignKey
            Relación muchos a uno, Maquina con el Proveedor.
        tipo_maquina : ForeignKey
            Relación muchos a uno, Maquina con el TipoMaquina.
        descripcion : CharField
            Almacena una breve descripción de la máquina.
        imagen_maquina : ImageField
            Almacena la dirección física de la imagen de la Máquina.
        negocio : ForeignKey
            Relación muchos a uno, Maquina con el Negocio.
        creado_por : ForeignKey
            Relación muchos a uno, Maquina con Usuario que Creó.
        actualizado_por : ForeignKey
            Relación muchos a uno, Maquina con Usuario que Actualizó.

    Args: 
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    nombre  = models.CharField(max_length=250, blank=True, null=True, verbose_name="Nombre Máquina")
    marca = models.ForeignKey(Marca, related_name='relMaquinaMarca', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Marca")
    proveedor = models.ForeignKey(Proveedor, related_name='relMaquinaProveedor', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Proveedor")
    tipo_maquina = models.ForeignKey(TipoMaquina, related_name='relMaquinaTipoMaquina', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Tipo Máquina")
    descripcion  = models.CharField(max_length=250, blank=True, null=True, verbose_name="Descripción")
    imagen_maquina = models.ImageField(upload_to=elimina_imagen_cargada, blank=True, null=True)
    negocio = models.ForeignKey(Negocio, related_name='relMaquinaNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    creado_por = models.ForeignKey(User, related_name='relMaquinaCreateUser', on_delete=models.CASCADE, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, related_name='relMaquinaUpdateUser', on_delete=models.CASCADE, null=True, blank=True)


    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve id, marca.
        """
        return '({}) {}'.format(self.id, self.marca)

    class Meta:
        verbose_name='Máquina'
        verbose_name_plural='Máquinas'
        ordering = ['-id']





class InventarioMaquinariaVentas(ControlCreaciones):
    """
    La clase InventarioMaquinariaVentas se utiliza para almacenar la lista de Máquinas Ventas.

    Attributes:
        maquina : ForeignKey
            Relación muchos a uno, InventarioMaquinariaVentas con el Maquina.
        precio : DecimalField
            Almacena el precio de la máquina.
        stock : IntegerField
            Almacena la cantidad de máquinas en el inventario.
        tipo_maquina : ForeignKey
            Relación muchos a uno, InventarioMaquinariaVentas con el TipoMaquina.
        negocio : ForeignKey
            Relación muchos a uno, InventarioMaquinariaVentas con el Negocio.
        creado_por : ForeignKey
            Relación muchos a uno, InventarioMaquinariaVentas con Usuario que Creó.
        actualizado_por : ForeignKey
            Relación muchos a uno, InventarioMaquinariaVentas con Usuario que Actualizó.

    Args: 
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    maquina = models.ForeignKey(Maquina, related_name='relInventarioMaquinariaVentasMaquina', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Máquina")
    precio = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Precio")
    stock = models.IntegerField(blank=True, null=True, verbose_name="Stock")
    #tipo_maquina = models.ForeignKey(TipoMaquina, related_name='relInventarioMaquinariaVentasTipoMaquina', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Tipo Máquina")
    
    negocio = models.ForeignKey(Negocio, related_name='relInventarioMaquinariaVentasNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    creado_por = models.ForeignKey(User, related_name='relInventarioMaquinariaVentasCreateUser', on_delete=models.CASCADE, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, related_name='relInventarioMaquinariaVentasUpdateUser', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve id, maquina.
        """
        return '({}) {}'.format(self.id, self.maquina)

    class Meta:
        verbose_name='Inventario Maquinaria Ventas'
        verbose_name_plural='Inventario Maquinaria Ventas'
        ordering = ['-id']






class IngresoCompras(ControlCreaciones):
    """
    La clase IngresoCompras se utiliza para almacenar las compras de Máquinas.

    Attributes:
        fecha_compra : DateField
            Almacena la fecha de la compra de la Máquina.
        maquina : ForeignKey
            Relación muchos a uno, IngresoCompras con la Máquina.
        precio : DecimalField
            Almacena el precio de la máquina.
        cantidad : IntegerField
            Almacena la cantidad de máquinas de la Compra.
        tipo_maquina : ForeignKey
            Relación muchos a uno, IngresoCompras con el TipoMaquina.
        negocio : ForeignKey
            Relación muchos a uno, IngresoCompras con el Negocio.
        creado_por : ForeignKey
            Relación muchos a uno, IngresoCompras con Usuario que Creó.
        actualizado_por : ForeignKey
            Relación muchos a uno, IngresoCompras con Usuario que Actualizó.

    Args: 
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    fecha_compra = models.DateField(null=True, blank=True, verbose_name="Fecha de Compra")

    maquina = models.ForeignKey(Maquina, related_name='relIngresoComprasMaquina', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Máquina")
    precio = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Precio")
    cantidad = models.IntegerField(blank=True, null=True, verbose_name="Cantidad")
    #tipo_maquina = models.ForeignKey(TipoMaquina, related_name='relIngresoComprasTipoMaquina', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Tipo Máquina")
    
    negocio = models.ForeignKey(Negocio, related_name='relIngresoComprasNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    creado_por = models.ForeignKey(User, related_name='relIngresoComprasCreateUser', on_delete=models.CASCADE, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, related_name='relIngresoComprasUpdateUser', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve id, maquina.
        """
        return '({}) {}'.format(self.id, self.maquina)

    class Meta:
        verbose_name='Ingreso de Compras'
        verbose_name_plural='Ingreso de Compras'
        ordering = ['-id']



# Alimenta al inventario
@receiver(post_save, sender=IngresoCompras) 
def fn_enviar_compra_a_inventario(sender, instance, **kwargs):

    # Instanciar el inventario y contar para ver si existe el producto en el inventario
    objInventarioMaquinariaVentas = InventarioMaquinariaVentas.objects.filter(maquina=instance.maquina, negocio=instance.negocio).count()

    # Sí es mayor a cero es porque existe, si es así sólo actualizar el registro del inventario
    if(objInventarioMaquinariaVentas > 0):
        InventarioMaquinariaVentas.objects.filter(maquina=instance.maquina, negocio=instance.negocio).update(stock=F('stock') + instance.cantidad)
    # Si no hay producto de este tipo en el inventario, entonces crearlo
    else:
        InventarioMaquinariaVentas.objects.create(  maquina=instance.maquina,
                                                    stock=instance.cantidad,
                                                    negocio=instance.negocio,
                                                    creado_por=instance.creado_por,
                                                    precio=(float(instance.precio)*1.30)
                                                    )
    







class InventarioMaquinariaAlquiler(ControlCreaciones):
    """
    La clase InventarioMaquinariaAlquiler se utiliza para almacenar la lista de Máquinas para Alquiler.

    Attributes:
        maquina : ForeignKey
            Relación muchos a uno, InventarioMaquinariaAlquiler con el Maquina.
        precio_por_dia : DecimalField
            Almacena el precio de la máquina por día de alquiler.
        baja : BooleanField
            Bandera que indica si la máquina ha sido dada de baja.
        fecha_baja : DateField
            Almacena la fecha de la baja de la máquina.
        disponible : BooleanField
            Bandera que indica si la máquina está disponible para alquiler.
        negocio : ForeignKey
            Relación muchos a uno, InventarioMaquinariaAlquiler con el Negocio.
        creado_por : ForeignKey
            Relación muchos a uno, InventarioMaquinariaAlquiler con Usuario que Creó.
        actualizado_por : ForeignKey
            Relación muchos a uno, InventarioMaquinariaAlquiler con Usuario que Actualizó.

    Args: 
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    maquina = models.ForeignKey(Maquina, related_name='relInventarioMaquinariaAlquilerMaquina', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Máquina")
    precio_por_dia = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Precio por Día")
    
    baja = models.BooleanField(default=False)
    fecha_baja = models.DateField(null=True, blank=True, verbose_name="Fecha de Baja")

    disponible = models.BooleanField(default=True)

    negocio = models.ForeignKey(Negocio, related_name='relInventarioMaquinariaAlquilerNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    creado_por = models.ForeignKey(User, related_name='relInventarioMaquinariaAlquilerCreateUser', on_delete=models.CASCADE, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, related_name='relInventarioMaquinariaAlquilerUpdateUser', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve id, maquina.
        """
        return '({}) {}'.format(self.id, self.maquina)

    class Meta:
        verbose_name='Inventario Maquinaria Alquiler'
        verbose_name_plural='Inventario Maquinaria Alquileres'
        ordering = ['-id']






class EstadoAlquiler(models.Model):
    """
    La clase EstadoAlquiler se utiliza para almacenar la lista Estados para los Alquileres.

    Attributes:
        nombre : CharField
            Nombre del Estado del Alquiler.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    estado_alquiler = models.CharField(max_length=150, blank=True, null=True, verbose_name="Estado del Alquiler")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id, estado_alquiler.
        """
        return '({}) {}'.format(self.id, self.estado_alquiler)

    class Meta:
        verbose_name='Estado Alquiler'
        verbose_name_plural='Estado Alquileres'
        ordering = ['-id']






class AlquilerMaquina(ControlCreaciones):
    """
    La clase AlquilerMaquina se utiliza para almacenar la ficha de Alquiler.

    Attributes:
        maquina_alquiler : ForeignKey
            Relación muchos a uno, AlquilerMaquina con el InventarioMaquinariaAlquiler.
        fecha_entrega : DateField
            Almacena la fecha de la entrega del alquiler.
        fecha_devolucion : DateField
            Almacena la fecha de la devolución del alquiler.
        observacion_entrega : CharField
            Almacena las observaciones de la entrega de la maquinaria.
        observacion_devolucion : CharField
            Almacena las observaciones de la devolución de la maquinaria.
        estado_alquiler : ForeignKey
            Relación muchos a uno, AlquilerMaquina con el EstadoAlquiler.
            Eje: 1 Lista para Facturar, 2 Lista para Entregar, 3 En Alquiler, 4 Devuelta
        devuelto : BooleanField
            Bandera que indica si la máquina ha sido devuelta del alquiler.
        anotaciones_seguimiento : TextField
            Almacena notas del seguimiento acerca del alquiler de la maquinaría.
        negocio : ForeignKey
            Relación muchos a uno, AlquilerMaquina con el Negocio.
        creado_por : ForeignKey
            Relación muchos a uno, AlquilerMaquina con Usuario que Creó.
        actualizado_por : ForeignKey
            Relación muchos a uno, AlquilerMaquina con Usuario que Actualizó.

    Args: 
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    maquina_alquiler = models.ForeignKey(InventarioMaquinariaAlquiler, related_name='relAlquilerMaquinaMaquina', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Máquina Alquiler")
    fecha_entrega = models.DateField(null=True, blank=True, verbose_name="Fecha de Entrega")
    fecha_devolucion = models.DateField(null=True, blank=True, verbose_name="Fecha Prevista de Devolución")

    observacion_entrega = models.CharField(max_length=250, blank=True, null=True, verbose_name="Observación de Entrega")
    observacion_devolucion = models.CharField(max_length=250, blank=True, null=True, verbose_name="Observación de Devolución")

    estado_alquiler = models.ForeignKey(EstadoAlquiler, related_name='relAlquilerMaquinaEstadoAlquiler', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Estado del Alquiler")

    devuelto = models.BooleanField(default=False)
    anotaciones_seguimiento = models.TextField(blank=True, null=True, verbose_name="Anotaciones Seguimiento")

    negocio = models.ForeignKey(Negocio, related_name='relAlquilerMaquinaNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    creado_por = models.ForeignKey(User, related_name='relAlquilerMaquinaCreateUser', on_delete=models.CASCADE, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, related_name='relAlquilerMaquinaUpdateUser', on_delete=models.CASCADE, null=True, blank=True)

    def fn_calcular_dias(self):
        lv_dias = None
        if self.fecha_devolucion and self.fecha_entrega:
            lv_dias = (self.fecha_devolucion - self.fecha_entrega).days
        
        return lv_dias

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve id, maquina.
        """
        return '({}) {}'.format(self.id, self.maquina_alquiler)

    class Meta:
        verbose_name='Alquiler Máquinas'
        verbose_name_plural='Alquileres de Máquinas'
        ordering = ['-id']



# Reservar vehículo
@receiver(pre_save, sender=AlquilerMaquina) 
def fn_reservar_maquina(sender, instance, **kwargs):
    
    if instance.maquina_alquiler:
        if(instance.maquina_alquiler.disponible is True):
            instance.maquina_alquiler.disponible = False
            instance.maquina_alquiler.save()


# Liberar vehículo
@receiver(pre_save, sender=AlquilerMaquina) 
def fn_liberar_maquina(sender, instance, **kwargs):
    
    if(instance.devuelto):
        if instance.maquina_alquiler:
            if(instance.maquina_alquiler.disponible is False):
                instance.maquina_alquiler.disponible = True
                instance.maquina_alquiler.save()




class DetalleFactura(ControlCreaciones):
    """
    La clase DetalleFactura se utiliza para almacenar el detalle de cada factura.
    
    Attributes:
        factura : ForeignKey
            Relación muchos a uno, DetalleFactura con Factura.
        es_compra : BooleanField
            Bandera para identificar si el detalle es una compra o alquiler.
        maquina_nueva : ForeignKey
            Relación muchos a uno, DetalleFactura con InventarioMaquinariaVentas.
        cantidad : IntegerField
            Indicador de la cantidad de maquinas para la venta o alquiler.
        precio : DecimalField
            Identifica el precio que tiene la máquina de la venta o alquiler.
        negocio : ForeignKey
            Relación muchos a uno, DetalleFactura con el Negocio.
        creado_por : ForeignKey
            Relación muchos a uno, DetalleFactura con Usuario que Creó.
        actualizado_por : ForeignKey
            Relación muchos a uno, DetalleFactura con Usuario que Actualizó.
        
    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    factura = models.ForeignKey(Factura, related_name='relDetalleFacturaVAMaquinariaFactura', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Factura")
    es_compra = models.BooleanField(default=True)

    maquina_nueva = models.ForeignKey(InventarioMaquinariaVentas, related_name='relDetalleFacturaInventarioMaquinariaVentas', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Máquina Nueva")
    ficha_alquiler = models.ForeignKey(AlquilerMaquina, related_name='relDetalleFacturaAlquilerMaquina', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Ficha Alquiler")
    cantidad = models.IntegerField(blank=True, null=True, verbose_name="Cantidad")
    precio = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, verbose_name="Precio")

    negocio = models.ForeignKey(Negocio, related_name='relDetalleFacturaVAMaquinariaNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    creado_por = models.ForeignKey(User, related_name='relDetalleFacturaVAMaquinariaCreateUser', on_delete=models.CASCADE, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, related_name='relDetalleFacturaVAMaquinariaUpdateUser', on_delete=models.CASCADE, null=True, blank=True)

    def fn_subtotal(self):
        return self.precio * self.cantidad


    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id, factura, es_compra.
        """
        return '({}) - ({}) - ({})'.format(self.id, self.factura, self.es_compra)

    class Meta:
        verbose_name='Detalle de Factura V.A. Maquinaria'
        verbose_name_plural='Detalle de Facturas V.A. Maquinaria'
        ordering = ['-id']




# Cuando se asigna una cantidad al detalle de la factura, se debe restar del stock del inventario.
@receiver(post_save, sender=DetalleFactura) 
def fn_restar_stock(sender, instance, **kwargs):
    
    # VALIDA SI SE CREO
    if kwargs.get('created', True):
        if (instance.es_compra is True):
            # Instanciar el InventarioMaquinariaVentas
            ObjInventario = InventarioMaquinariaVentas.objects.get(id=instance.maquina_nueva.id, negocio=instance.negocio)
            # Debitar el stock asignado al detalle
            ObjInventario.stock = ObjInventario.stock - instance.cantidad
            ObjInventario.save()
        
        if (instance.es_compra is False):
            # Instanciar el InventarioMaquinariaAlquiler
            ObjFichaAlquiler = AlquilerMaquina.objects.get(id=instance.ficha_alquiler.id, negocio=instance.negocio) # estado_alquiler
            ObjInventarioAlquiler = InventarioMaquinariaAlquiler.objects.get(id=ObjFichaAlquiler.maquina_alquiler.id, negocio=instance.negocio)

            # actualizar estado de la ficha de alquiler
            ObjFichaAlquiler.estado_alquiler = EstadoAlquiler.objects.get(id=2) # Lista para entrega, ya facturada
            ObjFichaAlquiler.save()

            # actualizar la disponibilidad de la máquina de alquiler
            ObjInventarioAlquiler.disponible = False
            ObjInventarioAlquiler.save()


# Cuando se elimina un producto del detalle de la factura, se debe restaurar el stock que se había debitado
@receiver(pre_delete, sender=DetalleFactura) 
def fn_restaurar_stock(sender, instance, **kwargs):
    
    if (instance.es_compra is True):
        # Instanciar el Inventario
        ObjInventario = InventarioMaquinariaVentas.objects.get(id=instance.maquina_nueva.id, negocio=instance.negocio)
        # Debitar el stock asignado al detalle
        ObjInventario.stock = ObjInventario.stock + instance.cantidad
        ObjInventario.save()
    
    if (instance.es_compra is False):
            # Instanciar el InventarioMaquinariaAlquiler
            ObjFichaAlquiler = AlquilerMaquina.objects.get(id=instance.ficha_alquiler.id, negocio=instance.negocio) # estado_alquiler
            ObjInventarioAlquiler = InventarioMaquinariaAlquiler.objects.get(id=ObjFichaAlquiler.maquina_alquiler.id, negocio=instance.negocio)

            # actualizar estado de la ficha de alquiler
            ObjFichaAlquiler.estado_alquiler = EstadoAlquiler.objects.get(id=1) # Lista para entrega, ya facturada
            ObjFichaAlquiler.save()

            # actualizar la disponibilidad de la máquina de alquiler
            ObjInventarioAlquiler.disponible = True
            ObjInventarioAlquiler.save()
