from django.db import models
from apps.registration.models import Negocio



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



class Proveedor(ControlCreaciones):
    """
    La clase Proveedor se utiliza para almacenar el catálogo de Proveedores.
    
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
        
    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    nombre_proveedor = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre Proveedor")
    nombre_contacto = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre del Contacto")
    telefono = models.IntegerField(blank=True, null=True, verbose_name="Teléfono")
    nit = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nit")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    negocio = models.ForeignKey(Negocio, related_name='relProveedoresNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id, nombre de proveedor, nombre de contacto.
        """
        return '({}) ({}) - ({})'.format(self.id, self.nombre_proveedor, self.nombre_contacto)

    class Meta:
        verbose_name='Proveedor'
        verbose_name_plural='Proveedores'
        ordering = ['-id']

