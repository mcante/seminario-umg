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






class Medidas(models.Model):
    """
    La clase Medidas se utiliza para almacenar la lista de las medidas para los productos que aplican.

    Attributes:
        medida : CharField
            Unidad de medida para el producto.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    medida = models.CharField(max_length=150, blank=True, null=True, verbose_name="Unidad de Medida")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve la medida.
        """
        return '({}) {}'.format(self.id, self.medida)

    class Meta:
        verbose_name='Medida'
        verbose_name_plural='Medidas'
        ordering = ['-id']








# Al eliminar una imagen_producto, también se eliminara fisicamente
def fn_elimina_imagen_cargada(instance, filename):
    try:
        old_instance = Producto.objects.get(pk=instance.pk)
        old_instance.adjuntar_boleta.delete()
    except:
        print('')
            
    return 'productos/{}_{}'.format(instance.id, filename)

class Producto(ControlCreaciones):
    """
    La clase Producto se utiliza para almacenar el catálogo de Productos.
    
    Attributes:
        nombre_proveedor : CharField
            Almacena el nombre del proveedor.
        nombre_contacto : CharField
            Almacena el nombre del contacto con el proveedor.
        telefono : IntegerField
            Almacena el número de teléfono del contacto.
        nit : TextField
            Identifica el número de contribuyente para la Superintendencia de Administración Tributaria.
        direccion : CharField
            Dirección del proveedor.
        negocio : ForeignKey
            Relación muchos a uno, Proveedor con el Negocio.
        creado_por : ForeignKey
            Relación muchos a uno, Producto con Usuario que Creó.
        actualizado_por : ForeignKey
            Relación muchos a uno, Producto con Usuario que Actualizó.
        
    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    nombre = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre del Producto")
    descripcion = models.CharField(max_length=150, blank=True, null=True, verbose_name="Descripción")
    proveedor = models.ForeignKey(Proveedor, related_name='relProductoProveedor', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Proveedor")
    imagen_producto = models.ImageField(upload_to=fn_elimina_imagen_cargada, blank=True, null=True)
    negocio = models.ForeignKey(Negocio, related_name='relProductoNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    creado_por = models.ForeignKey(User, related_name='relProductoCreateUser', on_delete=models.CASCADE, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, related_name='relProductoUpdateUser', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id, nombre del producto, nombre de proveedor.
        """
        return '({}) ({}) - ({})'.format(self.id, self.nombre, self.proveedor)

    class Meta:
        verbose_name='Producto'
        verbose_name_plural='Productos'
        ordering = ['-id']











class Inventario(ControlCreaciones):
    """
    La clase Inventario se utiliza para almacenar el Inventario del Negocio.
    
    Attributes:
        factura : ForeignKey
            Relación muchos a uno, DetalleFactura con Factura.
        producto : ForeignKey
            Relación muchos a uno, DetalleFactura con Producto.
        cantidad : IntegerField
            Indicador de la cantidad de productos para la venta.
        precio : DecimalField
            Identifica el precio que tiene el producto actualmente.
        negocio : ForeignKey
            Relación muchos a uno, DetalleFactura con el Negocio.
        creado_por : ForeignKey
            Relación muchos a uno, DetalleFactura con Usuario que Creó.
        actualizado_por : ForeignKey
            Relación muchos a uno, DetalleFactura con Usuario que Actualizó.
        
    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    producto = models.ForeignKey(Producto, related_name='relInventarioProducto', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Producto")
    precio = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, verbose_name="Precio Producto")
    stock = models.IntegerField(blank=True, null=True, verbose_name="Stock")
    unidad_medida = models.ForeignKey(Medidas, related_name='relInventarioMedidas', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Unidad de Medida")

    negocio = models.ForeignKey(Negocio, related_name='relInventarioPlantaNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    creado_por = models.ForeignKey(User, related_name='relInventarioPlantaCreateUser', on_delete=models.CASCADE, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, related_name='relInventarioPlantaUpdateUser', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id, producto, stock.
        """
        return '({}) ({}) - ({})'.format(self.id, self.producto, self.stock)

    class Meta:
        verbose_name='Inventario'
        verbose_name_plural='Inventario'
        ordering = ['-id']





class IngresoCompras(ControlCreaciones):
    """
    La clase IngresoCompras se utiliza para almacenar las compras de Máquinas.

    Attributes:
        fecha_compra : DateField
            Almacena la fecha de la compra de la Máquina.
        producto : ForeignKey
            Relación muchos a uno, IngresoCompras con la Producto.
        precio : DecimalField
            Almacena el precio del producto.
        cantidad : IntegerField
            Almacena la cantidad de Productos de la Compra.
        unidad_medida : ForeignKey
            Relación muchos a uno, IngresoCompras con el Medidas.
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

    producto = models.ForeignKey(Producto, related_name='relIngresoComprasProducto', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Producto")
    precio = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Precio Venta")
    precio_compra = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, verbose_name="Precio Compra")
    cantidad = models.IntegerField(blank=True, null=True, verbose_name="Cantidad")
    unidad_medida = models.ForeignKey(Medidas, related_name='relIngresoComprasMedidas', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Medida")
    
    negocio = models.ForeignKey(Negocio, related_name='relIngresoComprasPlantasNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    creado_por = models.ForeignKey(User, related_name='relIngresoComprasPlantasCreateUser', on_delete=models.CASCADE, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, related_name='relIngresoComprasPlantasUpdateUser', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve id, producto.
        """
        return '({}) {}'.format(self.id, self.producto)

    class Meta:
        verbose_name='Ingreso de Compras'
        verbose_name_plural='Ingreso de Compras'
        ordering = ['-id']



# Alimenta al inventario
@receiver(post_save, sender=IngresoCompras) 
def fn_enviar_compra_a_inventario_plantas(sender, instance, **kwargs):

    # Instanciar el inventario y contar para ver si existe el producto en el inventario
    objInventarioVentas = Inventario.objects.filter(producto=instance.producto, negocio=instance.negocio).count()

    # Sí es mayor a cero es porque existe, si es así sólo actualizar el registro del inventario
    if(objInventarioVentas > 0):
        Inventario.objects.filter(producto=instance.producto, negocio=instance.negocio).update(stock=F('stock') + instance.cantidad)
    # Si no hay producto de este tipo en el inventario, entonces crearlo
    else:
        Inventario.objects.create(  producto=instance.producto,
                                    stock=instance.cantidad,
                                    unidad_medida=instance.unidad_medida,
                                    negocio=instance.negocio,
                                    creado_por=instance.creado_por,
                                    precio=instance.precio
                                    )
    





class DetalleFactura(ControlCreaciones):
    """
    La clase DetalleFactura se utiliza para almacenar el detalle de cada factura.
    
    Attributes:
        factura : ForeignKey
            Relación muchos a uno, DetalleFactura con Factura.
        producto : ForeignKey
            Relación muchos a uno, DetalleFactura con Producto.
        cantidad : IntegerField
            Indicador de la cantidad de productos para la venta.
        precio : DecimalField
            Identifica el precio que tiene el producto actualmente.
        negocio : ForeignKey
            Relación muchos a uno, DetalleFactura con el Negocio.
        creado_por : ForeignKey
            Relación muchos a uno, DetalleFactura con Usuario que Creó.
        actualizado_por : ForeignKey
            Relación muchos a uno, DetalleFactura con Usuario que Actualizó.
        
    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    factura = models.ForeignKey(Factura, related_name='relPlantasDetalleFacturaFactura', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Factura")
    producto = models.ForeignKey(Producto, related_name='relDetalleFacturaProducto', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Producto")
    cantidad = models.IntegerField(blank=True, null=True, verbose_name="Cantidad")
    precio = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, verbose_name="Precio Producto")

    negocio = models.ForeignKey(Negocio, related_name='relDetalleFacturaPlantaNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    creado_por = models.ForeignKey(User, related_name='relDetalleFacturaPlantaCreateUser', on_delete=models.CASCADE, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, related_name='relDetalleFacturaPlantaUpdateUser', on_delete=models.CASCADE, null=True, blank=True)

    def fn_subtotal(self):
        return self.precio * self.cantidad


    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id, factura, producto.
        """
        return '({}) ({}) - ({})'.format(self.id, self.factura, self.producto)

    class Meta:
        verbose_name='Detalle de Factura'
        verbose_name_plural='Detalle de Facturas'
        ordering = ['-id']



# Cuando se asigna una cantidad al detalle de la factura, se debe restar del stock del inventario.
@receiver(post_save, sender=DetalleFactura) 
def fn_restar_stock(sender, instance, **kwargs):
    
    # VALIDA SI SE CREO
    if kwargs.get('created', True):
        # Instanciar el Inventario
        ObjInventario = Inventario.objects.get(producto=instance.producto, negocio=instance.negocio)
        # Debitar el stock asignado al detalle
        ObjInventario.stock = ObjInventario.stock - instance.cantidad
        ObjInventario.save()

# Cuando se elimina un producto del detalle de la factura, se debe restaurar el stock que se había debitado
@receiver(pre_delete, sender=DetalleFactura) 
def fn_restaurar_stock(sender, instance, **kwargs):
    
    # Instanciar el Inventario
    ObjInventario = Inventario.objects.get(producto=instance.producto, negocio=instance.negocio)
    # Debitar el stock asignado al detalle
    ObjInventario.stock = ObjInventario.stock + instance.cantidad
    ObjInventario.save()
