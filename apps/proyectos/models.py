from django.db import models
from django.contrib.auth.models import User

from apps.factura.models import Factura
from apps.registration.models import Negocio
from apps.clientes.models import Cliente
from apps.gastos.models import RegistroGastos, TipoGasto

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete



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





class TipoProyecto(models.Model):
    """
    La clase TipoProyecto se utiliza para almacenar la lista de los tipos de proyecto.

    Attributes:
        nombre : CharField
            Nombre del Tipo Proyecto.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    nombre = models.CharField(max_length=150, blank=True, null=True, verbose_name="Tipo de Proyecto")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el nombre del tipo de proyecto.
        """
        return '({}) {}'.format(self.id, self.nombre)

    class Meta:
        verbose_name='Tipo de Proyecto'
        verbose_name_plural='Tipos de Proyecto'
        ordering = ['-id']









class Proyecto(ControlCreaciones):
    """
    La clase Proyecto se utiliza para almacenar los Proyecto de Servicios de Construcción.
    
    Attributes:
        cliente : ForeignKey
            Relación muchos a uno, Proyecto con Cliente.
        nombre_proyecto : CharField
            Almacena el nombre del proyecto.
        fecha_inicio : DateField
            Almacena la fecha en la que inicia el Proyecto.
        fecha_fin : DateField
            Almacena la fecha en la que finaliza el Proyecto.
        tipo_proyecto : ForeignKey
            Relación muchos a uno, Proyecto con Tipo Proyecto.
        descripcion : TextField
            Almacena detalles que describen el proyecto.
        presupuesto_estimado : DecimalField
            Almacena el presupuesto estimado del proyecto.
        gastos_totales : DecimalField
            Almacena los gastos totales acumulados del proyecto.
        empleado : ForeignKey
            Relación muchos a uno, Proyecto con el Empleado asignado.
        completado : BooleanField
            Bandera, indicador de Pedido Completada.
        negocio : ForeignKey
            Relación muchos a uno, Proyecto con el Negocio.
        creado_por : ForeignKey
            Relación muchos a uno, Proyecto con Usuario que Creó.
        actualizado_por : ForeignKey
            Relación muchos a uno, Proyecto con Usuario que Actualizó.

    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    cliente = models.ForeignKey(Cliente, related_name='relProyectoCliente', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Cliente")
    nombre_proyecto = models.CharField(max_length=250, blank=True, null=True, verbose_name="Nombre del Proyecto")
    fecha_inicio = models.DateField(null=True, blank=True, verbose_name="Fecha de Inicio")
    fecha_fin = models.DateField(null=True, blank=True, verbose_name="Fecha de Fin")
    tipo_proyecto = models.ForeignKey(TipoProyecto, related_name='relProyectoTipoProyecto', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Tipo Proyecto")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción del Proyecto")
    presupuesto_estimado = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Presupuesto Estimado")
    gastos_totales = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Gastos Totales")
    empleado = models.ForeignKey(User, related_name='relProyectoUserEmpleado', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Empleado Asignado")
    completado = models.BooleanField(default=False)

    negocio = models.ForeignKey(Negocio, related_name='relProyectoNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    creado_por = models.ForeignKey(User, related_name='relProyectoCreateUser', on_delete=models.CASCADE, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, related_name='relProyectoUpdateUser', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id, nombre_proyecto, cliente.
        """
        return '({}) {} - {}'.format(self.id, self.nombre_proyecto, self.cliente)

    class Meta:
        verbose_name='Proyecto'
        verbose_name_plural='Proyectos'
        ordering = ['-id']






# Al eliminar una imagen_producto, también se eliminara fisicamente
def fn_elimina_imagen_cargada(instance, filename):
    try:
        old_instance = Documentos.objects.get(pk=instance.pk)
        old_instance.documento_adjunto.delete()
    except:
        print('')
            
    return 'proyecto_documentos/{}_{}'.format(instance.proyecto.id, filename)

class Documentos(ControlCreaciones):
    """
    La clase Documentos se utiliza para almacenar la lista de Documentos de cada Proyecto.
    
    Attributes:
        proyecto : ForeignKey
            Relación muchos a uno, Documentos con Proyecto.
        titulo_documento : CharField
            Almacena el título del Documentos.
        descripcion : TextField
            Almacena la descripción del documento.
        documento_adjunto : FileField
            Almacena la ruta del documento adjunto.
        creado_por : ForeignKey
            Relación muchos a uno, Documentos con Usuario que Creó.
        actualizado_por : ForeignKey
            Relación muchos a uno, Documentos con Usuario que Actualizó.
        
    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    proyecto = models.ForeignKey(Proyecto, related_name='relDocumentosProyecto', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Proyecto")
    titulo_documento = models.CharField(max_length=150, blank=True, null=True, verbose_name="Título del Documento")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    documento_adjunto = models.FileField(upload_to=fn_elimina_imagen_cargada, blank=True, null=True)
    
    creado_por = models.ForeignKey(User, related_name='relDocumentosCreateUser', on_delete=models.CASCADE, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, related_name='relDocumentosUpdateUser', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id, proyecto, titulo_documento.
        """
        return '({}) ({}) - ({})'.format(self.id, self.proyecto, self.titulo_documento)

    class Meta:
        verbose_name='Documento'
        verbose_name_plural='Documentos'
        ordering = ['-id']



# Al eliminar una imagen_producto, también se eliminara fisicamente
def fn_elimina_imagen_cargada_gastos(instance, filename):
    try:
        old_instance = Documentos.objects.get(pk=instance.pk)
        old_instance.documento_adjunto.delete()
    except:
        print('')
            
    return 'proyecto_gastos/{}_{}'.format(instance.proyecto.id, filename)

class GastosProyecto(ControlCreaciones):
    """
    La clase GastosProyecto se utiliza para almacenar la lista de los gastos del Proyecto.
    
    Attributes:
        proyecto : ForeignKey
            Relación muchos a uno, GastosProyecto con Proyecto.
        titulo_gasto : CharField
            Almacena el título del Gasto que generó el proyecto.
        descripcion : TextField
            Almacena la descripción del gasto.
        fecha_gasto : DateField
            Almacena la fecha del gasto.
        monto : DecimalField
            Almacena el monto del gasto.
        autorizado_por : ForeignKey
            Relación muchos a uno, GastosProyecto con Usuario que autoriza.
        documento_adjunto : FileField
            Almacena la ruta del gasto adjunto.
        creado_por : ForeignKey
            Relación muchos a uno, GastosProyecto con Usuario que Creó.
        actualizado_por : ForeignKey
            Relación muchos a uno, GastosProyecto con Usuario que Actualizó.
        
    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    proyecto = models.ForeignKey(Proyecto, related_name='relGastosProyectoProyecto', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Proyecto")
    titulo_gasto = models.CharField(max_length=150, blank=True, null=True, verbose_name="Título del Gasto")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción")
    fecha_gasto = models.DateField(null=False, blank=False, verbose_name="Fecha de Gasto")
    monto = models.DecimalField(max_digits=15, decimal_places=2, null=False, blank=False, verbose_name="Monto")
    autorizado_por = models.ForeignKey(User, related_name='relGastosProyectoUserEmpleado', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Autorizado Por")
    documento_adjunto = models.FileField(upload_to=fn_elimina_imagen_cargada_gastos, blank=True, null=True)

    negocio = models.ForeignKey(Negocio, related_name='relGastosProyectoNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    creado_por = models.ForeignKey(User, related_name='relGastosProyectoCreateUser', on_delete=models.CASCADE, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, related_name='relGastosProyectoUpdateUser', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id, proyecto, titulo_gasto.
        """
        return '({}) - ({}) - ({})'.format(self.id, self.proyecto, self.titulo_gasto)

    class Meta:
        verbose_name='Gasto del Proyecto'
        verbose_name_plural='Gastos del Proyecto'
        ordering = ['-id']




# Cuando agrega un nuevo gasto, se suma al total de gastos del Proyecto
@receiver(post_save, sender=GastosProyecto) 
def fn_acumular_a_gastos_totales_proyecto(sender, instance, **kwargs):
    
    # VALIDA SI SE CREO
    if kwargs.get('created', True):
        # Instanciar el Proyecto
        ObjProyecto = Proyecto.objects.get(id=instance.proyecto.id, negocio=instance.negocio)
        
        # Suma el monto del gasto a los gastos totales del proyecto
        try:
            ObjProyecto.gastos_totales = ObjProyecto.gastos_totales + instance.monto            
        except:
            ObjProyecto.gastos_totales = instance.monto
        
        #import pdb; pdb.set_trace()
        ObjProyecto.save()

        
        # Registrar el gasto en la tabla general.
        RegistroGastos.objects.create(
                                        tipo_gasto = TipoGasto.objects.get(pk=5),
                                        fecha_gasto = instance.fecha_gasto,
                                        monto = instance.monto,
                                        descripcion_gasto = instance.titulo_gasto,
                                        autorizado_por = instance.autorizado_por,
                                        negocio = instance.negocio,
                                        creado_por = instance.creado_por
                                    )



class DetalleFacturaEntregables(ControlCreaciones):
    """
    La clase DetalleFacturaEntregables se utiliza para almacenar la lista de los gastos del Proyecto.
    
    Attributes:
        proyecto : ForeignKey
            Relación muchos a uno, DetalleFacturaEntregables con Proyecto.
        titulo_gasto : CharField
            Almacena el título del Gasto que generó el proyecto.
        descripcion : TextField
            Almacena la descripción del gasto.
        fecha_gasto : DateField
            Almacena la fecha del gasto.
        monto : DecimalField
            Almacena el monto del gasto.
        autorizado_por : ForeignKey
            Relación muchos a uno, DetalleFacturaEntregables con Usuario que autoriza.
        documento_adjunto : ImageField
            Almacena la ruta del gasto adjunto.
        creado_por : ForeignKey
            Relación muchos a uno, DetalleFacturaEntregables con Usuario que Creó.
        actualizado_por : ForeignKey
            Relación muchos a uno, DetalleFacturaEntregables con Usuario que Actualizó.
        
    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    factura = models.ForeignKey(Factura, related_name='relFacturaProyecto', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Factura")
    proyecto = models.ForeignKey(Proyecto, related_name='relDetalleFacturaEntregablesProyecto', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Proyecto")
    fecha_entregable = models.DateField(null=False, blank=False, verbose_name="Fecha del Entregable")
    monto = models.DecimalField(max_digits=10, decimal_places=2, null=False, blank=False, verbose_name="Monto")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción del Entregable")

    negocio = models.ForeignKey(Negocio, related_name='relDetalleFacturaEntregablesNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")
    
    creado_por = models.ForeignKey(User, related_name='relDetalleFacturaEntregablesCreateUser', on_delete=models.CASCADE, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, related_name='relDetalleFacturaEntregablesUpdateUser', on_delete=models.CASCADE, null=True, blank=True)

    def fn_subtotal(self):
        return self.monto

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id, proyecto, titulo_gasto.
        """
        return '({}) - ({}) - ({})'.format(self.id, self.proyecto, self.factura)

    class Meta:
        verbose_name='Detalle de Entregable Facturado'
        verbose_name_plural='Detalles de Entregables Facturados'
        ordering = ['-id']


# Cuando agrega un nuevo entregable, se suma al total de la Factura
@receiver(post_save, sender=DetalleFacturaEntregables) 
def fn_acumular_suma_total_factura(sender, instance, **kwargs):
    
    # VALIDA SI SE CREO
    if kwargs.get('created', True):
        # Instanciar el Proyecto
        ObjDetalleProyecto = Factura.objects.get(id=instance.factura.id, negocio=instance.negocio)
        # Suma el monto del gasto a los gastos totales del proyecto
        ObjDetalleProyecto.monto_total = ObjDetalleProyecto.monto_total + instance.monto
        ObjDetalleProyecto.save()
