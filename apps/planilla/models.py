from django.db import models

from django.contrib.auth.models import User
from apps.registration.models import Negocio
from django.utils import timezone #Agregada por mi para el manejo de la fecha
from decimal import Decimal
from datetime import datetime

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



class Puesto(models.Model):
    """
    La clase Puesto se utiliza para almacenar la lista de los puestos.

    Attributes:
        nombre : CharField
            Nombre del Tipo puesto.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    nombre = models.CharField(max_length=150, blank=True, null=True, verbose_name="Puesto")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el nombre del tipo de proyecto.
        """
        return '({}) {}'.format(self.id, self.nombre)

    class Meta:
        verbose_name='Tipo de Puesto'
        verbose_name_plural='Tipos de Puesto'
        ordering = ['-id']





class Empleados(ControlCreaciones):
    primer_nombre = models.CharField(max_length=250, blank=True, null=True, verbose_name="Primer Nombre")
    segundo_nombre = models.CharField(max_length=250, blank=True, null=True, verbose_name="Segundo Nombre")
    apellidos = models.CharField(max_length=250, blank=True, null=True, verbose_name="Apellidos")
    email = models.EmailField(max_length = 250, blank=True, null=True, verbose_name="Correo")
    fecha_ingreso = models.DateField(null=True, blank=True, verbose_name="Fecha de Ingreso")
    fecha_terminacion = models.DateField(null=True, blank=True, verbose_name="Fecha de Terminación")
    salario_base = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, null=True, blank=True, verbose_name="Salario Base")
    bonificacion_de_ley = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, null=True, blank=True, verbose_name="Bonificación de Ley")
    descuentos = models.DecimalField(max_digits=15, decimal_places=2, default=0.00, null=True, blank=True, verbose_name="Descuentos")
    puesto = models.ForeignKey(Puesto, related_name='relSalariosPuesto', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Puesto")
    activo = models.BooleanField(default=True)
    
    negocio = models.ForeignKey(Negocio, related_name='relEmpleadosNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    creado_por = models.ForeignKey(User, related_name='relEmpleadosUserCreadoPor', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Creado Por")
    actualizado_por = models.ForeignKey(User, related_name='relEmpleadosUserActualizadoPor', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Actualizado Por")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            str: Devuelve el nombre nombre completo del usuario.
        """
        return '({}) {} {}'.format(self.id, self.primer_nombre, self.apellidos)

    class Meta:
        verbose_name='Empleado'
        verbose_name_plural='Empleados'
        ordering = ['-id']
    
    # Muestra el nombre completo
    def get_full_name(self):
        fullname = ''
        if(self.primer_nombre is not None):
            fullname = fullname + str(self.primer_nombre)
        if(self.segundo_nombre is not None):
            fullname = fullname + ' ' + str(self.segundo_nombre)
        if(self.apellidos is not None):
            fullname = fullname + ' '+ str(self.apellidos)
        
        return '{}'.format(fullname)




class TipoPago(models.Model):
    """
    La clase TipoPago almacena el catálogo de los tipos de pago, como por ejemplo:
    Salario mensual, Aguinaldo, Bono 14.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.

    Attributes:
        nombre_tipo_pago : CharField
            Describe el tipo de pago.

    """
    nombre_tipo_pago = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nombre del tipo de pago")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            str: Devuelve el nombre del tipo de pago.
        """
        return '({}) {}'.format(self.id, self.nombre_tipo_pago)

    class Meta:
        verbose_name='Tipo de Pago'
        verbose_name_plural='Tipos de Pago'
        ordering = ['-id']



class Meses(models.Model):
    """
    La clase Meses contiene el catálogo de todos los meses del año, ejemplo:
    Enero, Febrero, Marzo, ...Diciembre.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.

    Attributes:
        nombre_tipo_pago : CharField
            Describe el tipo de pago.

    """
    nombre_mes = models.CharField(max_length=50, blank=True, null=True, verbose_name="Mes")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            str: Devuelve el nombre del mes.
        """
        return '({}) {}'.format(self.id, self.nombre_mes)

    class Meta:
        verbose_name='Mes'
        verbose_name_plural='Meses'
        ordering = ['id']




class EncabezadoPlanilla(ControlCreaciones):
    """
    La clase EncabezadoPlanilla almacena la información de la planilla mensual de salarios.

    Attributes:
        tipo_pago : ForeignKey
            Relación muchos a uno, Asigna Tipo de Pago. Refiere al catálogo de pagos.
        mes : ForeignKey
            Relación muchos a uno, Asigna Mes. Refiere a la planilla del mes.
        generar_automaticamente : BooleanField
            Bandera que indica si la planilla debe ser generada automáticamente.
            Tomara la lista de empleados y los agregará a la planilla.
        ha_sido_generado : BooleanField
            Bandera que indica si ya ha sido generada la planilla automática para evitar que se vuelva a generar.
        negocio : ForeignKey
            Relación muchos a uno, Asigna el Negocio.
        creado_por : ForeignKey
            Relación muchos a uno, Asigna Usuario que creó el registro.
        actualizado_pro : ForeignKey
            Relación muchos a uno, Asigna Usuario que modificó el registro.
    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    tipo_pago = models.ForeignKey(TipoPago, related_name='relEncabezadoPlanillaTipoPago', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Tipo de Pago")
    mes = models.ForeignKey(Meses, related_name='relEncabezadoPlanillaMeses', on_delete=models.CASCADE, blank=True, null=True, verbose_name="EncabezadoPlanilla del Mes")
    generar_automaticamente = models.BooleanField(default=False)
    ha_sido_generado = models.BooleanField(default=False)

    completado = models.BooleanField(default=False)

    negocio = models.ForeignKey(Negocio, related_name='relEncabezadoPlanillaNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    creado_por = models.ForeignKey(User, related_name='relEncabezadoPlanillaUserCreadoPor', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Creado Por")
    actualizado_por = models.ForeignKey(User, related_name='relEncabezadoPlanillaUserActualizadoPor', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Actualizado Por")
    

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            str: Devuelve el nombre del empleado y el mes de la planilla.
        """
        return '({}) {} - {}'.format(self.id, self.tipo_pago.nombre_tipo_pago, self.mes)

    class Meta:
        verbose_name='Encabezado Planilla Mensual'
        verbose_name_plural='Encabezado de Planillas'
        ordering = ['id']

# EXISTE UN SIGNAL AL FINAL PARA GENERAR LA PLANILLA



class Planilla(ControlCreaciones):
    """
    La clase Planilla almacena la información de la planilla mensual de salarios.

    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    
    Attributes:
        encabezado_planilla : ForeignKey
            Relación muchos a uno, Asinga el Encabezado de la Planilla.
        empleado : ForeignKey
            Relación muchos a uno, Asigna Usuario.
        tipo_pago : ForeignKey
            Relación muchos a uno, Asigna Tipo de Pago. Refiere al catálogo de pagos.
        mes : ForeignKey
            Relación muchos a uno, Asigna Mes. Refiere a la planilla del mes.
        salario : DecimalField
            Define el salario devengado que tiene un usuario.
        bonificacion_de_ley : DecimalField
            Define la bonificación de ley que tiene un usuario.
        igss : DecimalField
            Define el descuento del IGSS al que aplica el usuario.
        bonos_extra : DecimalField
            Define los bonos extras como comisionesal que aplica el usuario.
        descuentos : DecimalField
            Define el descuentos generales al que aplica el usuario.
        negocio : ForeignKey
            Relación muchos a uno, Asigna el Negocio.
        creado_por : ForeignKey
            Relación muchos a uno, Asigna Usuario que creó el registro.
        actualizado_pro : ForeignKey
            Relación muchos a uno, Asigna Usuario que modificó el registro.

    """
    encabezado_planilla = models.ForeignKey(EncabezadoPlanilla, related_name='relPlanillaEncabezadoPlanilla', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Encabezado de Planilla")
    empleado = models.ForeignKey(Empleados, related_name='relPlanillaEmpleados', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Empleado")
    
    tipo_pago = models.ForeignKey(TipoPago, related_name='relPlanillaTipoPago', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Tipo de Pago")
    mes = models.ForeignKey(Meses, related_name='relPlanillaMeses', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Planilla del Mes")

    salario = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, null=True, blank=True, verbose_name="Salario Base")
    bonificacion_de_ley = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, null=True, blank=True, verbose_name="Bonificación de Ley")
    igss = models.DecimalField(max_digits=6, decimal_places=2, default=0.00, null=True, blank=True, verbose_name="IGSS")
    bonos_extra = models.DecimalField(max_digits=6, default=0.00, decimal_places=2, null=True, blank=True, verbose_name="Bonos Extra")
    descuentos = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, null=True, blank=True, verbose_name="Descuentos")

    negocio = models.ForeignKey(Negocio, related_name='relPlanillaNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    creado_por = models.ForeignKey(User, related_name='relPlanillaUserCreadoPor', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Creado Por")
    actualizado_por = models.ForeignKey(User, related_name='relPlanillaUserActualizadoPor', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Actualizado Por")
    

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            str: Devuelve el nombre del empleado y el mes de la planilla.
        """
        return '({}) {} - {}'.format(self.id, self.empleado.primer_nombre, self.empleado.apellidos, self.mes)

    class Meta:
        verbose_name='Cuerpo Planilla Mensual'
        verbose_name_plural='Cuerpo de Planillas'
        ordering = ['id']



@receiver(pre_save, sender=Planilla)
def fn_salario_descuentos(sender, instance, **kwargs):
    """
    Función que carga el salario configurado y calcula el IGSS.

    Args:
        sender (clase Planilla): Clase Planilla que invoca la función signal.
        instance (instancia de la clase): Objecto o instancia que ejecutó al signal.
    """

    # Recuperar el objecto salario
    ObjSalario = Empleados.objects.get(id=instance.empleado.id)

    if(ObjSalario):
        instance.salario = ObjSalario.salario_base
        instance.bonificacion_de_ley = ObjSalario.bonificacion_de_ley
        instance.descuentos = ObjSalario.descuentos
        
        # Solo si el tipo de pago es Salario Mensual, equivalente a 1
        if(instance.tipo_pago.id == 1):
            instance.igss = float(ObjSalario.salario_base + ObjSalario.bonificacion_de_ley) * 0.0483
        else:
            instance.igss = 0.00



@receiver(post_save, sender=EncabezadoPlanilla)
def fn_generar_planilla(sender, instance, **kwargs):
    """
    Función genera la planilla basada en la lista de empleados activos.

    Args:
        sender (clase Planilla): Clase EncabezadoPlanilla que invoca la función signal.
        instance (instancia de la clase): Objecto o instancia que ejecutó al signal.
    """

    if(instance.generar_automaticamente is True and instance.ha_sido_generado is False):

        # Recuperar la lista de empleados activos
        ObjEmpleados = Empleados.objects.filter(activo=True, negocio=instance.negocio)

        for obj in ObjEmpleados:
            Planilla.objects.create(
                encabezado_planilla = instance,
                empleado = obj,
                tipo_pago = instance.tipo_pago,
                mes = instance.mes,
                salario = obj.salario_base,
                bonificacion_de_ley = obj.bonificacion_de_ley,
                descuentos = obj.descuentos,
                negocio = instance.negocio,
                creado_por = instance.creado_por,
            )
        
        instance.ha_sido_generado = True
        instance.save()
