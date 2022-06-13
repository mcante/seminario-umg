from django.db import models

from django.contrib.auth.models import User
from apps.registration.models import Perfil, Negocio

from django.dispatch import receiver
from django.db.models.signals import post_save, pre_save, pre_delete, post_delete


#Generar Key o llave
import string, random



class Cliente(models.Model):
    """
    La clase Cliente almacena la información de los clientes de la empresa.

    Attributes:
        nombre_empresa : CharField
            Identifica el Nombre de la Empresa asociada al cliente.
        nombre_contacto : CharField
            Identifica el Nombre del contacto con la empresa.
        email : EmailField
            Correo electrónico del Cliente.
        telefono : IntegerField
            Teléfono del Cliente.
        extension : IntegerField
            Extensión para el número de teléfono sólo cuando aplica.
        nit : CharField
            Identifica el número de contribuyente para la Superintendencia de Administración Tributaria.
        direccion : TextField
            Dirección del Cliente o Empresa.
        key_access : CharField
            Llave de acceso asignada al cliente para acceder al sistema.
        empleado_asignado : ForeignKey
            Relación muchos a uno, Indentifica al empleado asignado para atender al cliente.
        creado : DateTimeField
            Fecha y hora de creación.
        actualizado : DateTimeField
            Fecha y hora de modificación.

    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones
        la cual almacena información de campos comúnes.
    """
    nombre_empresa = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre de la Empresa")
    nombre_contacto = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre del Contacto")
    email = models.EmailField(max_length = 254, blank=True, null=True, verbose_name="Correo")
    telefono = models.IntegerField(blank=True, null=True, verbose_name="Teléfono")
    extension = models.IntegerField(blank=True, null=True, verbose_name="Extensión")
    nit = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nit")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    key_access = models.CharField(max_length=30, blank=True, null=True, verbose_name="Llave de Acceso")
    empleado_asignado = models.ForeignKey(User, related_name='relClienteUser', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Empleado Asignado")
    
    creado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    actualizado = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")    
    
    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el nombre de la Empresa.
        """
        return '({}) {}'.format(self.id, self.nombre_empresa)
    

    class Meta:
        verbose_name='Cliente'
        verbose_name_plural='Clientes'
        ordering = ['-id']



@receiver(pre_save, sender=Cliente) 
def fn_generar_llave_acceso(sender, instance, **kwargs):
    
    if (instance.key_access is None):
        chars=string.ascii_letters + string.digits
        instance.key_access = ''.join(random.choice(chars) for _ in range(8))




class Telefonos(models.Model):
    """
    La clase Telefonos almacena más números de teléno asociados al Cliente.
    Permite indicar un número como preferido el cual se actualizará en la clase de Cliente.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.

    Attributes:
        cliente : ForeignKey
            Relación muchos a uno, Identifica el Cliente asociado al número de teléfono.
        numero_telefono : IntegerField
            Teléfono del Cliente.
        marcar_preferico : BooleanField
            Identifica si el número será el principal que debe mostrarse en el perfil del Cliente
    """
    cliente = models.ForeignKey(Cliente, related_name='relTelefonosCliente', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Cliente")
    numero_telefono = models.IntegerField(blank=True, null=True, verbose_name="Número de Teléfono")
    marcar_preferico = models.BooleanField(default=False, verbose_name="Marcar como preferido")
    
    def __str__(self):
        return '{}'.format(self.numero_telefono)
    
    class Meta:
        verbose_name='Teléfono'
        verbose_name_plural='Teléfonos'


@receiver(pre_save, sender=Telefonos) 
def fn_numero_preferido(sender, instance, **kwargs):
    """
    Función, cada vez que se cree o modifique cualquier número de teléfono se ejecutará sólo si está seleccionado como preferido.
    Actualiza el perfil del Cliente con el número preferido y limpia cualquier otro de la lista de preferidos.

    Args:
        sender (clase Telefonos): Clase Telefonos que invoca la función signal.
        instance (instancia de la clase): Objecto o instancia que ejecutó al signal.
    """
    
    if (instance.marcar_preferico):
        
        # Obtener la lista de números guardados del Cliente.
        lista_numeros = Telefonos.objects.filter(cliente=instance.cliente, marcar_preferico = True)
        # Obtiene una instancia del Cliente
        ObjCliente = Cliente.objects.get(pk=instance.cliente.id)
        
        # Actualiza el número preferido en la persona
        ObjCliente.telefono = instance.numero_telefono
        ObjCliente.save() #Guardar

        # Desmarca cualquier otro número que esté como preferido en la agenda de contactos de la persona
        for numeroAntiguo in lista_numeros:
            numeroAntiguo.marcar_preferico = False #Quitar número preferido
            numeroAntiguo.save() #Guardar
    




class NegocioCliente(models.Model):
    """
    La clase NegocioCliente almacena la relación entre El Negocio y el Cliente. 
    Se utilizará para almacenar los negocios a los que podrá estar asociado cada cliente.

    Attributes:
        negocio : ForeignKey
            Relación muchos a uno, Asigna el Negocio o Empresa.
        cliente : ForeignKey
            Relación muchos a uno, Asigna Cliente.
        
    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    negocio = models.ForeignKey(Negocio, related_name='relNegocioClienteNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")
    cliente = models.ForeignKey(Cliente, related_name='relNegocioClienteCliente', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Cliente")
    vendedor = models.ForeignKey(User, related_name='relNegocioClienteVendedor', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Vendedor Asignado")
    
    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el nombre del Negocio.
        """
        return '({}) - ({}) - ({})'.format(self.negocio, self.negocio.giro_negocio, self.cliente)
    
    class Meta:
        unique_together = (("negocio", "cliente"),)
        verbose_name='Asignar Negocio a Cliente'
        verbose_name_plural='Asignar Negocio a Cliente'
        ordering = ['-id']



"""
    Agrega el Negocio al Cliente
"""
@receiver(post_save, sender=Cliente) 
def fn_asigna_negocio(sender, instance, **kwargs):

    # VALIDA SI SE CREO
    if kwargs.get('created', True):

        objPerfil = Perfil.objects.get(user=instance.empleado_asignado)
        print(objPerfil.negocio)

        NegocioCliente.objects.create( cliente=instance, negocio=objPerfil.negocio, vendedor=instance.empleado_asignado)






class Contacto(models.Model):
    """
    La clase Contacto almacena la información de los contactos que han llenado el formulario desde la página pública.

    Attributes:
        negocio : ForeignKey
            Relación muchos a uno, Indentifica el giro de negocio que el contacto desea comunicarse.
        nombre_contacto : CharField
            Identifica el Nombre del contacto con la empresa.
        email : EmailField
            Correo electrónico del contacto.
        telefono : IntegerField
            Teléfono del Cliente.
        nombre_empresa : CharField
            Identifica el Nombre de la Empresa asociada al contacto.
        mensaje : TextField
            Mensaje o razón de contacto.
        creado : DateTimeField
            Fecha y hora de creación.
        actualizado : DateTimeField
            Fecha y hora de modificación.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    negocio = models.ForeignKey(Negocio, related_name='relContactoNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Servicio")
    nombre_contacto = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre del Contacto")
    email = models.EmailField(max_length = 254, blank=True, null=True, verbose_name="Correo")
    telefono = models.IntegerField(blank=True, null=True, verbose_name="Teléfono")
    nombre_empresa = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre de la Empresa")
    mensaje = models.TextField(blank=True, null=True, verbose_name="Mensaje")

    atentido = models.BooleanField(default=False, verbose_name="Atendido")

    creado = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    actualizado = models.DateTimeField(auto_now=True, verbose_name="Fecha de edición")    
    
    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id y nombre_contacto.
        """
        return '({}) {}'.format(self.id, self.nombre_contacto)
    

    class Meta:
        verbose_name='Contacto'
        verbose_name_plural='Contactos'
        ordering = ['-id']