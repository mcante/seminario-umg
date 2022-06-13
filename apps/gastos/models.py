from django.db import models
from django.contrib.auth.models import User
from apps.registration.models import Negocio

# Create your models here.





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



class TipoGasto(models.Model):
    """
    La clase TipoGasto se utiliza para almacenar los tipos de gastos.
    Ejemplo: Compra, salarios, Ejecución de proyecto, Mantenimiento, etc.

    Attributes:
        nombre_gasto : CharField
            Nombre del tipo de Gasto.
        negocio : ForeignKey
            Relación muchos a uno, TipoGasto con el Negocio.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    nombre_gasto = models.CharField(max_length=150, blank=True, null=True, verbose_name="Tipo de Gasto")
    negocio = models.ForeignKey(Negocio, related_name='relTipoGastoNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el tipo de gasto.
        """
        return '({}) {}'.format(self.id, self.nombre_gasto)
    
    class Meta:
        verbose_name='Tipo de Gasto'
        verbose_name_plural='Tipos de Gasto'
        ordering = ['-id']




class RegistroGastos(ControlCreaciones):
    """
    La clase RegistroGastos se utiliza para almacenar los gastos generados por Negocio.
    
    Attributes:
        tipo_gasto : ForeignKey
            Relación muchos a uno, Registro de Gastos con Tipo de Gasto.
        fecha_gasto : DateField
            Almacena la fecha en la que se registra el gasto.
        monto : DecimalField
            Almacena el total del gasto.
        descripcion_gasto : TextField
            Almacena una descripción general del gasto.
        autorizado_por : ForeignKey
            Relación muchos a uno, RegistroGastos con el usuario que autorizó el gasto.
        negocio : ForeignKey
            Relación muchos a uno, RegistroGastos con el Negocio.
        creado_por : ForeignKey
            Relación muchos a uno, RegistroGastos con el usuario que creó la gasto.
        actualizado_por : ForeignKey
            Relación muchos a uno, RegistroGastos con el usuario que modificó la gasto.

    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    tipo_gasto = models.ForeignKey(TipoGasto, related_name='relRegistroGastosTipoGasto', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Tipo de Gasto")
    fecha_gasto = models.DateField(null=False, blank=False, verbose_name="Fecha de Gasto")
    monto = models.DecimalField(max_digits=15, decimal_places=2, null=False, blank=False, verbose_name="Monto Gasto")
    descripcion_gasto = models.TextField(blank=True, null=True, verbose_name="Descripción del Gasto")
    autorizado_por = models.ForeignKey(User, related_name='relRegistroGastosUser', on_delete=models.CASCADE, null=True, blank=True)
    negocio = models.ForeignKey(Negocio, related_name='relRegistroGastosNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")
    
    creado_por = models.ForeignKey(User, related_name='relRegistroGastosCreateUser', on_delete=models.CASCADE, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, related_name='relRegistroGastosUpdateUser', on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id, nombre del gasto, fecha y monto.
        """
        return '({}) ({}) - {} - ({})'.format(self.id, self.tipo_gasto.nombre_gasto, self.fecha_gasto, self.monto)

    class Meta:
        verbose_name='Registro de Gastos'
        verbose_name_plural='Registro de Gastos'
        ordering = ['-id']
