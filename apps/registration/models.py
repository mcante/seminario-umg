from django.db import models

from django.contrib.auth.models import User
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






class Pais(models.Model):
    """
    La clase País se utiliza para almacenar la lista de países.
    
    Attributes:
        nombre : CharField
            Nombre del Pais que identifica.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    nombre = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nombre del País")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el nombre del país.
        """
        return '({}) {}'.format(self.id, self.nombre)

    class Meta:
        verbose_name='País'
        verbose_name_plural='Países'
        ordering = ['-id']



class Departamento(models.Model):
    """
    La clase Departamento se utiliza para almacenar la lista de departamentos de cada país.
    
    Attributes:
        nombre : CharField
            Nombre del Departamento.
        pais : ForeignKey
            Relación uno a muchos, Departamento con País.
    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    nombre = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nombre del Departamento")
    pais = models.ForeignKey(Pais, related_name='relDepartamentoPais', on_delete=models.CASCADE, blank=True, null=True, verbose_name="País")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el nombre del departamento.
        """
        return '({}) {}'.format(self.id, self.nombre)

    class Meta:
        verbose_name='Departamento'
        verbose_name_plural='Departamentos'
        ordering = ['-id']


class Municipio(models.Model):
    """
    La clase Municipio se utiliza para almacenar la lista de Municipios de cada departamento.

    Attributes:
        nombre : CharField
            Nombre del Municipio que identifica.
        deparamento : ForeignKey
            Relación uno a muchos, Municipio con Departamento.
    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    nombre = models.CharField(max_length=100, blank=True, null=True, verbose_name="Nombre del Municipio")
    deparamento = models.ForeignKey(Departamento, related_name='relMunicipioDepartamento', on_delete=models.CASCADE, blank=False, null=False, verbose_name="Departamento")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el nombre del municipio.
        """
        return '({}) {}'.format(self.id, self.nombre)

    class Meta:
        verbose_name='Municipio'
        verbose_name_plural='Municipios'
        ordering = ['-id']



class GiroNegocio(ControlCreaciones):
    """
    La clase Giro de Negocio almacena el catálogo de cada Giro de Negocio de la empresa.

    Attributes:
        nombre_giro : CharField
            Nombre del Giro de Negocio
        descripcion : TextField
            Descripción del Negocio

    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    nombre_giro = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre del Giro de Negocio")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción del Negocio")
    
    
    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el nombre del Giro de Negocio.
        """
        return '{}'.format(self.nombre_giro)
    
    class Meta:
        verbose_name='Giro de Negocio'
        verbose_name_plural='Giros de Negocio'
        ordering = ['-id']





class Negocio(ControlCreaciones):
    """
    La clase Negocio almacena la información de cada Negocio de la empresa.

    Attributes:
        nombre_negocio : CharField
            Identifica el Nombre del Negocio.
        telefono : IntegerField
            Almacena el número de teléfono0
        extension : IntegerField
            Extensión del número de teléfono sólo cuando aplica.
        email : EmailField
            Correo electrónico.
        municipio : ForeignKey
            Relación muchos a uno, Identifica el Municipio al que pertenece el Negocio.
        direccion : TextField
            Dirección de la ubicación del Negocio.
        giro_negocio : ForeignKey
            Relación muchos a uno, Identifica el Giro de Negocial al que pertenece.

    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones
        la cual almacena información de campos comúnes.
    """
    nombre_negocio = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre del Negocio")
    telefono = models.IntegerField(blank=True, null=True, verbose_name="Teléfono")
    extension = models.IntegerField(blank=True, null=True, verbose_name="Extensión")
    email = models.EmailField(max_length = 254, blank=True, null=True, verbose_name="Correo")
    municipio = models.ForeignKey(Municipio, related_name='relNegocioMunicipio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Municipio")
    direccion = models.TextField(blank=True, null=True, verbose_name="Dirección")
    giro_negocio = models.ForeignKey(GiroNegocio, related_name='relNegocioGiroNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Giro de Negocio")
    
    
    
    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el nombre del negocio y el giro de negocio.
        """
        return '({}) {} - {}'.format(self.id, self.nombre_negocio, self.giro_negocio)
    

    class Meta:
        verbose_name='negocio'
        verbose_name_plural='negocios'
        ordering = ['-id']




class TipoEmpleado(ControlCreaciones):
    """
    La clase Tipo de Empleado  almacena el catálogo de los tipos de empelados de la empresa.
    Ejemplo: Supervisor, Vendedor, Contador, Secretaria, Piloto, 

    Attributes:
        nombre : CharField
            Nombre del tipo de empleado
        descripcion : TextField
            Descripción del Tipo de Empleado

    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    nombre = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre del Tipo de Empleado")
    descripcion = models.TextField(blank=True, null=True, verbose_name="Descripción del Empleado")
    negocio = models.ForeignKey(Negocio, related_name='relTipoEmpleadoNegocio', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Negocio")
    
    
    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el nombre del Tipo de Empleado.
        """
        return '({}) {}'.format(self.id, self.nombre)
    
    class Meta:
        verbose_name='Tipo de Empleado'
        verbose_name_plural='Tipos de Empleado'
        ordering = ['-id']



def elimina_imagen_cargada(instance, filename):
    """
    Función que eliminara físicamente alguna imagen que contenga el mismo nombre que el que se pasa como argumento.

    Args:
        instance (clase Perfil): Instancia de la clase de que invoca.
        filename (str): Nombre de la ruta del archivo físico al que apunta la imagen.

    Returns:
        str: Devuelve la dirección física de la imagen
    """
    old_instance = Perfil.objects.get(pk=instance.pk)
    old_instance.imagen.delete()
    return 'perfiles/' + filename



class Perfil(ControlCreaciones):
    """
    Este modelo Perfil almacena la informacion de los perfiles extendidos de usuario.

    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    
    Attributes:
        user : OneToOneField
            Relación uno a uno con el usuario y el perfil.
        imagen : ImageField
            Campo para almacenar ruta de la imagen del usuario.
        celular : IntegerField
            Campo para almacenar el número de celular del usaurio.
        negocio : ForeignKey
            Relación muchos a uno, Usuario a Negocio.
        activo : BooleanField
            Campo indicador para el estado del usuario.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True, related_name='relPerfilUsuario')
    imagen = models.ImageField(upload_to=elimina_imagen_cargada, blank=True, null=True)
    celular = models.IntegerField(blank=True, null=True, verbose_name="Celular")
    negocio = models.ForeignKey(Negocio, related_name='relPerfilNegocio', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Negocio")
    tipo_empleado = models.ForeignKey(TipoEmpleado, related_name='relPerfilTipoEmpleado', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Tipo de Empleado")
    activo = models.BooleanField(default=True)

    

    def get_email(self):
        """Función que devuelve el correo electrónico del registro de Usuarios.

        Returns:
            str: Devuelve correo electrónico.
        """
        return self.user.email
    
    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el nombre completo del usuario y el userName.
        """
        return '{}  ({})'.format(self.user.get_full_name(), self.user)
        
    class Meta:
        verbose_name='perfil'
        verbose_name_plural='perfiles'
        ordering = ['-user']


# Signal para crear el perfil luego de crear un nuevo usuario.
@receiver(post_save, sender=User)
def fn_crea_perfil(sender, instance, **kwargs):
    """
    Función Signal para crear el perfil luego de crear un nuevo usuario.
    Se ejecuta después de guardar.

    Args:
        sender (clase User): Clase usuario que invoca la función signal.
        instance (instancia de la clase): Objecto o instancia que ejecutó al signal.
    """
    if kwargs.get('created', False):
        Perfil.objects.get_or_create(user=instance)
        #print("Se ha creado el perfil del usuario creado")


@receiver(pre_save, sender=Perfil)
def fn_file_avatar(sender, instance, **kwargs):
    """
    Función que al eliminar una imagen del registro, también se eliminara físicamente.
    Se ejecuta antes de guardar.

    Args:
        sender (clase Perfil): Clase Perfil que invoca la función signal.
        instance (instancia de la clase): Objecto o instancia que ejecutó al signal.
    """
    if(instance.imagen == ''):
        file_instance = Perfil.objects.get(pk=instance.pk)
        file_instance.imagen.delete()


@receiver(post_save, sender=Perfil)
def fn_actualiza_usuario_perfil(sender, instance, **kwargs):
    """
    Función Signal para actualizar el usuario a partir del perfil.
    Se ejecuta después de guardar.

    Args:
        sender (clase Perfil): Clase Perfil que invoca la función signal.
        instance (instancia de la clase): Objecto o instancia que ejecutó al signal.
    """
    
    # Recuperar el objecto Usuario
    ObjUsuario = User.objects.get(pk=instance.user.id)
    # Actualizar el estado de activo
    ObjUsuario.is_active = instance.activo
    ObjUsuario.save() #Guardar






class NegocioUsuario(ControlCreaciones):
    """
    La clase NegocioUsuario almacena la relación entre el Negocio, Giro de Negocio y el Usuario. 
    Se utilizará para almacenar los negocios y giros a los que podrá estar asociado cada usuario.

    Attributes:
        negocio : ForeignKey
            Relación muchos a uno, Asigna el Negocio.
        perfil_usuario : ForeignKey
            Relación muchos a uno, Asigna Perfil.
        preferido : BooleanField
            Indicador de preferencia para setear un default para el inicio de sesión.
    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    negocio = models.ForeignKey(Negocio, related_name='relNegocioUsuarioNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")
    perfil_usuario = models.ForeignKey(Perfil, related_name='relNegocioUsuarioPerfil', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Usuario")
    preferido = models.BooleanField(default=True)
    
    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el nombre del negocio y su giro.
        """
        return '({}) - ({}) - ({})'.format(self.negocio, self.negocio.giro_negocio, self.perfil_usuario)
    
    class Meta:
        unique_together = (("negocio", "perfil_usuario"),)
        verbose_name='Asignar Negocio a Usuario'
        verbose_name_plural='Asignar Negocio a Usuario'
        ordering = ['-id']



@receiver(pre_save, sender=NegocioUsuario)
def fn_predetermina_negocio(sender, instance, **kwargs):
    """
    Función que predetermina el Negocio si se marca como preferido.

    Args:
        sender (clase NegocioUsuario): Clase NegocioUsuario que invoca la función signal.
        instance (instancia de la clase): Objecto o instancia que ejecutó al signal.
    """

    # Recuperar el objecto Accesos segun el perfil
    ObjAccesos = NegocioUsuario.objects.filter(perfil_usuario=instance.perfil_usuario)
    lv_cantidad_negocios = ObjAccesos.count()

    # Si hay más negocios asignados y el nuevo es el preferido, entonces limpiar todos los preferidos anteriores.
    if(lv_cantidad_negocios > 0 and instance.preferido == True):
        
        # Limpiar cualquier otro negocio que esté como predeterminado
        for obj in ObjAccesos:
            if(obj.preferido == True):
                obj.preferido = False
                obj.save()
        
        instance.preferido == True

    if kwargs.get('created', True):
        ObjPerfil = Perfil.objects.get(id=instance.perfil_usuario.id)

        ObjPerfil.negocio = instance.negocio
        ObjPerfil.save()




@receiver(pre_delete, sender=NegocioUsuario)
def fn_elimina_negocio_preferido_perfil(sender, instance, **kwargs):
    """
    Función Signal para actualizar el negocio predeterminado del Perfil después de ser eliminado.
    La eliminará del Perfil sólo si la que se está eliminando es igual a la del perfil.

    Args:
        Args:
        sender (clase NegocioUsuario): Clase NegocioUsuario que invoca la función signal.
        instance (instancia de la clase): Objecto o instancia que ejecutó al signal.
    """
    
    # Recuperar el objecto Accesos segun el perfil
    ObjPerfil = Perfil.objects.get(id=instance.perfil_usuario.id)

    
    if(instance.negocio.id == ObjPerfil.negocio.id):
        ObjPerfil.negocio = None
        ObjPerfil.save()







class Presupuesto(ControlCreaciones):
    """
    La clase Presupuesto almacena la información del presupuesto de cada Negocio.

    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    
    Attributes:
        presupuesto_anual : DecimalField
            Almacena el presupuesto anual asignado al negocio.
        excedente : DecimalField
            Almacena el excedente o lo que sobró del año anterior.
        anio : IntegerField
            Almacena el año al cual hace referencia el negocio.
        negocio : ForeignKey
            Relación muchos a uno, Asigna el Negocio.
        creado_por : ForeignKey
            Relación muchos a uno, Asigna Usuario que creó el registro.
        actualizado_por : ForeignKey
            Relación muchos a uno, Asigna Usuario que modificó el registro.

    """
    presupuesto_anual = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Presepuesto Anual")
    excedente = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, verbose_name="Excedente")
    anio = models.IntegerField(blank=True, null=True, verbose_name="Año")

    negocio = models.ForeignKey(Negocio, related_name='relPresupuestoNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    creado_por = models.ForeignKey(User, related_name='relPresupuestoUserCreadoPor', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Creado Por")
    actualizado_por = models.ForeignKey(User, related_name='relPresupuestoUserActualizadoPor', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Actualizado Por")
    

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            str: Devuelve el año y presupuesto.
        """
        return '({})-{}'.format(self.anio, self.presupuesto_anual)

    class Meta:
        verbose_name='Presupuesto'
        verbose_name_plural='Presupuestos'
        ordering = ['id']


