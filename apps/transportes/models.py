from django.db import models
from django.contrib.auth.models import User

from apps.factura.models import Factura
from apps.registration.models import Negocio

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






class Linea(models.Model):
    """
    La clase Linea se utiliza para almacenar la lista de Lineas para vehículos.

    Attributes:
        nombre : CharField
            Nombre de la Marca.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    nombre = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre Linea")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el nombre de la Linea.
        """
        return '({}) {}'.format(self.id, self.nombre)

    class Meta:
        verbose_name='Linea'
        verbose_name_plural='Lineas'
        ordering = ['-id']




class TipoVehiculo(models.Model):
    """
    La clase TipoVehiculo se utiliza para almacenar los tipos de vehículos.

    Attributes:
        nombre : CharField
            Almacena el tipo de vehículo.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    tipo_vehiculo = models.CharField(max_length=150, blank=True, null=True, verbose_name="Tipo de Vehículo")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el nombre del tipo de vehículo.
        """
        return '({}) {}'.format(self.id, self.tipo_vehiculo)

    class Meta:
        verbose_name='Tipo Vehiculo'
        verbose_name_plural='Tipos Vehiculo'
        ordering = ['-id']





class TransmisionVehiculo(models.Model):
    """
    La clase TransmisionVehiculo se utiliza para almacenar los tipos de transmisión de vehículos.

    Attributes:
        transmision_vehiculo : CharField
            Almacena el tipo de transmisión de vehículos.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    transmision_vehiculo = models.CharField(max_length=150, blank=True, null=True, verbose_name="Transmisión de Vehículo")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el nombre del tipo de transmisión de vehículo.
        """
        return '({}) {}'.format(self.id, self.transmision_vehiculo)

    class Meta:
        verbose_name='Transmisión vehículo'
        verbose_name_plural='Transmisión Vehículos'
        ordering = ['-id']






class DispositivoGPS(models.Model):
    """
    La clase DispositivoGPS se utiliza para almacenar los dispositivos GPS.

    Attributes:
        identificador : CharField
            Almacena el identificador del GPS.
        activo : BooleanField
            Bandera para identificar si el dispositivo está activo o no.
        velocidad_max_permitida : PositiveIntegerField
            Especifica la velocidad máxima que puede alcanzar un vehículo, luego de eso enviará alertas de velocidad.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    identificador = models.CharField(max_length=150, blank=True, null=True, verbose_name="Identificador del GPS")
    activo = models.BooleanField(default=True)
    velocidad_max_permitida = models.PositiveIntegerField(default=80, blank=True, null=True, verbose_name="Velocidad máxima permitida")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el nombre del identificador del GPS.
        """
        return '({}) {}'.format(self.id, self.identificador)

    class Meta:
        verbose_name='Dispositivo GPS'
        verbose_name_plural='Dispositivos GPS'
        ordering = ['-id']






class LogVelocidadesGPS(models.Model):
    """
    La clase LogVelocidadesGPS se utiliza para almacenar el log de las velocidades de navegación de los dispositivos GPS.

    Attributes:
        dispositivo_gps : ForeignKey
            Relación muchos a uno, LogVelocidadesGPS con DispositivoGPS.
        velocidad_km : IntegerField
            Almacena la velocidad registrado expresada en kilometros.
        latitud : CharField
            Almacena las coordenadas referentes a la latitud.
        longitud : CharField
            Almacena las coordenadas referentes a la longitud.
        velocidad_alertada : BooleanField
            Bandera que se activa si el vehículo ha sobrepasado la velocidad permitida
        creado : DateTimeField
            Almacena el registro de fecha y hora.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """

    dispositivo_gps = models.ForeignKey(DispositivoGPS, related_name='relLogVelocidadesGPSDispositivoGPS', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Dispositivo GPS")
    velocidad_km = models.IntegerField(blank=True, null=True, verbose_name="Velocidad km")

    latitud = models.CharField(max_length=150, blank=True, null=True, verbose_name="Latitud")
    longitud = models.CharField(max_length=150, blank=True, null=True, verbose_name="Longitud")

    velocidad_alertada = models.BooleanField(default=False)

    creado = models.DateTimeField(auto_now_add=True, verbose_name="Creado")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve id y dispositivo del log velocidades.
        """
        return '({}) {}'.format(self.id, self.dispositivo_gps)

    class Meta:
        verbose_name='Log Velocidades GPS'
        verbose_name_plural='Log Velocidades GPS'
        ordering = ['-id']


# Valida la velocidad máxima permitida
@receiver(pre_save, sender=LogVelocidadesGPS) 
def fn_velocidad_maxima(sender, instance, **kwargs):
    
    # Asegurar que exista un dispositivo gps
    if instance.dispositivo_gps:
        # Validar si la velocidad del vehículo es mayor a la permitida 
        if (instance.velocidad_km > instance.dispositivo_gps.velocidad_max_permitida):
            instance.velocidad_alertada = True





class LogTiemposGPS(ControlCreaciones):
    """
    La clase LogTiemposGPS se utiliza para almacenar el log de los tiempos de navegación de los dispositivos GPS.
    Cuando un vehículo se enciende recibe una señal de inicio de la ruta.
    Cuando un vehículo se apaga recibe una señal de fin de la ruta.

    Attributes:
        dispositivo_gps : ForeignKey
            Relación muchos a uno, LogTiemposGPS con DispositivoGPS.
        registro_inicio : DateTimeField
            Almacena el registro de fecha y hora inicio.
        latitud_inicio : CharField
            Almacena las coordenadas referentes a la latitud inicio.
        longitud_inicio : CharField
            Almacena las coordenadas referentes a la longitud inicio.
        registro_fin : DateTimeField
            Almacena el registro de fecha y hora fin.
        latitud_fin : CharField
            Almacena las coordenadas referentes a la latitud fin.
        longitud_fin : CharField
            Almacena las coordenadas referentes a la longitud fin.

    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """

    dispositivo_gps = models.ForeignKey(DispositivoGPS, related_name='relLogTiemposGPSDispositivoGPS', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Dispositivo GPS")
    
    registro_inicio = models.DateTimeField(null=True, blank=True, verbose_name="Fecha y Hora Inicio")
    latitud_inicio = models.CharField(max_length=150, blank=True, null=True, verbose_name="Latitud Inicio")
    longitud_inicio = models.CharField(max_length=150, blank=True, null=True, verbose_name="Longitud Inicio")

    registro_fin = models.DateTimeField(null=True, blank=True, verbose_name="Fecha y Hora Fin")
    latitud_fin = models.CharField(max_length=150, blank=True, null=True, verbose_name="Latitud Fin")
    longitud_fin = models.CharField(max_length=150, blank=True, null=True, verbose_name="Longitud Fin")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve id y dispositivo del log de tiempos.
        """
        return '({}) {}'.format(self.id, self.dispositivo_gps)

    class Meta:
        verbose_name='Log Tiempos GPS'
        verbose_name_plural='Log Tiempos GPS'
        ordering = ['-id']





# Al eliminar una imagen_producto, también se eliminara fisicamente
def fn_elimina_imagen_cargada(instance, filename):
    try:
        old_instance = InventarioVehiculo.objects.get(pk=instance.pk)
        old_instance.imagen_vehiculo.delete()
    except:
        pass
            
    return 'vehiculos/{}_{}'.format(instance.id, filename)

class InventarioVehiculo(ControlCreaciones):
    """
    La clase InventarioVehiculo se utiliza para almacenar el Inventario de Vechículos del Negocio.
    
    Attributes:
        fecha_ingreso : DateField
            Almacena la fecha en la que ingresó el vehículo al inventario.
        marca : ForeignKey
            Relación muchos a uno, InventarioVehiculo con Marca.
        linea : ForeignKey
            Relación muchos a uno, InventarioVehiculo con Línea.
        modelo : IntegerField
            Almacena el modelo o año del vehículo.
        tipo_vehiculo : ForeignKey
            Relación muchos a uno, InventarioVehiculo con tipo_vehiculo, ejemplo: camión, panel, etc.
        tipo_transmision : ForeignKey
            Relación muchos a uno, InventarioVehiculo con tipo_transmision, ejemplo: automática, manual, triptronic.
        color : CharField
            Almacena el color.
        cilindraje : IntegerField
            Almacena el cilindraje.
        numero_chasis : IntegerField
            Almacena el número de chasis.
        tonelaje : IntegerField
            Almacena las tonaladas del vehículo.
        placa : CharField
            Almacena la placa del vehículo.
        disponible : BooleanField
            Bandera para indicar si el vehículo está disponbile para viajes.
        permiso_fronterizo : BooleanField
            Bandera para indicar si el vehículo posee permiso internacional.
        dispositivo_gps : ForeignKey
            Relación muchos a uno, InventarioVehiculo con el dispositivo_gps.
        baja : BooleanField
            Bandera para indicar si el vehículo ha sido dado de baja del inventario.
        fecha_baja : DateField
            Almacena la fecha de la baja del inventario.
        negocio : ForeignKey
            Relación muchos a uno, InventarioVehiculo con el Negocio.
        creado_por : ForeignKey
            Relación muchos a uno, InventarioVehiculo con Usuario que Creó.
        actualizado_por : ForeignKey
            Relación muchos a uno, InventarioVehiculo con Usuario que Actualizó.
        
    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    fecha_ingreso = models.DateField(null=True, blank=True, verbose_name="Fecha Ingreso")

    marca = models.ForeignKey(Marca, related_name='relInventarioVehiculoMarca', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Marca")
    linea = models.ForeignKey(Linea, related_name='relInventarioVehiculoLinea', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Linea")
    modelo = models.IntegerField(blank=True, null=True, verbose_name="Modelo")
    tipo_vehiculo = models.ForeignKey(TipoVehiculo, related_name='relInventarioVehiculoTipoVehiculo', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Tipo Vehículo")
    tipo_transmision = models.ForeignKey(TransmisionVehiculo, related_name='relInventarioVehiculoTransmisionVehiculo', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Tipo Transmisión")

    color = models.CharField(max_length=50, blank=True, null=True, verbose_name="Color")
    cilindraje = models.IntegerField(blank=True, null=True, verbose_name="Cilindraje")
    numero_chasis = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número de Chasis")
    tonelaje = models.IntegerField(blank=True, null=True, verbose_name="Tonelaje")
    placa = models.CharField(max_length=50, blank=True, null=True, verbose_name="Placa")
    disponible = models.BooleanField(default=True)
    permiso_fronterizo = models.BooleanField(default=True)
    
    dispositivo_gps = models.ForeignKey(DispositivoGPS, related_name='relInventarioVehiculoDispositivoGPS', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Dispositivo GPS")

    baja = models.BooleanField(default=False)
    fecha_baja = models.DateField(null=True, blank=True, verbose_name="Fecha Baja")

    imagen_vehiculo = models.ImageField(upload_to=fn_elimina_imagen_cargada, blank=True, null=True)
    
    negocio = models.ForeignKey(Negocio, related_name='relInventarioVehiculoPlantaNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    creado_por = models.ForeignKey(User, related_name='relInventarioVehiculoPlantaCreateUser', on_delete=models.CASCADE, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, related_name='relInventarioVehiculoPlantaUpdateUser', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id, marca, modelo.
        """
        return '({}) ({}) - ({})'.format(self.id, self.marca, self.modelo)

    class Meta:
        verbose_name='Inventario Vehiculo'
        verbose_name_plural='Inventario Vehiculos'
        ordering = ['-id']








class AsignacionTarifa(ControlCreaciones):
    """
    La clase AsignacionTarifa se utiliza para almacenar las tarifas asignadas a cada vehículo, tarifa nacional o internacional.

    Attributes:
        vehiculo : ForeignKey
            Relación muchos a uno, AsignacionTarifa con InventarioVehiculo.
        fecha_autorizacion : DateField
            Almacena la fecha en la que se autoriza una tarifa en el sistema.
        precio_por_kilometro : DecimalField
            Almacena el precio autorizado.
        es_nacional : BooleanField
            Bandera para saber si la tarifa es nacional o internacional.

    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """

    vehiculo = models.ForeignKey(InventarioVehiculo, related_name='relAsignacionTarifaInventarioVehiculo', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Vehículo")
    fecha_autorizacion = models.DateField(null=True, blank=True, verbose_name="Fecha Autorización")
    precio_por_kilometro = models.DecimalField(max_digits=6, decimal_places=2, null=False, blank=False, verbose_name="Precio por Kilómetro")
    es_nacional = models.BooleanField(default=True)

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve id y vehiculo.
        """
        return '({}) {}'.format(self.id, self.vehiculo)

    class Meta:
        verbose_name='Log Tiempos GPS'
        verbose_name_plural='Log Tiempos GPS'
        ordering = ['-id']











class Rutas(ControlCreaciones):
    """
    La clase Rutas se utiliza para almacenar para el transporte.
    
    Attributes:
        factura : ForeignKey
            Relación muchos a uno, InventarioVehiculo con Factura.
        vehiculo : ForeignKey
            Relación muchos a uno, InventarioVehiculo con InventarioVehiculo.
        piloto : ForeignKey
            Relación muchos a uno, InventarioVehiculo con Piloto/User.
        fecha_salida_predio : DateField
            Almacena la fecha en la que el vehículo sale del predio.
        fecha_entrada_predio : DateField
            Almacena la fecha en la que el vehículo entra a predio.
        kilometraje_salida : IntegerField
            Almacena el kilometraje de salida.
        kilometraje_entrada : IntegerField
            Almacena el kilometraje de entrada.
        kilometros_recorridos : IntegerField
            Almacena el kilometraje del total recorrido.
        direccion_recoleccion : TextField
            Almacena la dirección para la recolección.
        contacto_recoleccion : TextField
            Almacena el contacto para la recolección.
        fecha_hora_recoleccion : DateTimeField
            Almacena la fecha y hora de la recolección.
        direccion_entrega : TextField
            Almacena la dirección de entrega de la ruta.
        fecha_hora_entrega : DateTimeField
            Almacena la fecha y hora de la entrega.
        contacto_entrega : TextField
            Almacena el nombre del contacto para la entrega.
        es_nacional : BooleanField
            Bandera para indicar si la ruta es internacional.
        completada : BooleanField
            Bandera para indicar si la ruta ha sido completada.
        negocio : ForeignKey
            Relación muchos a uno, Rutas con el Negocio.
        creado_por : ForeignKey
            Relación muchos a uno, Rutas con Usuario que Creó.
        actualizado_por : ForeignKey
            Relación muchos a uno, Rutas con Usuario que Actualizó.
    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    factura = models.ForeignKey(Factura, related_name='relRutasFactura', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Factura")
    vehiculo = models.ForeignKey(InventarioVehiculo, related_name='relRutasInventarioVehiculo', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Vehículo")
    piloto = models.ForeignKey(User, related_name='relRutasUser', on_delete=models.CASCADE, null=True, blank=True)
    
    fecha_salida_predio = models.DateField(null=True, blank=True, verbose_name="Fecha de Salida del Predio")
    fecha_entrada_predio = models.DateField(null=True, blank=True, verbose_name="Fecha de Entrada al Predio")
    
    kilometraje_salida = models.IntegerField(blank=True, null=True, verbose_name="kilometraje Salida")
    kilometraje_entrada = models.IntegerField(blank=True, null=True, verbose_name="kilometraje Entrada")
    kilometros_recorridos = models.IntegerField(blank=True, null=True, verbose_name="kilometros Recorridos")

    direccion_recoleccion = models.TextField(blank=True, null=True, verbose_name="Dirección de Recolección")
    contacto_recoleccion = models.TextField(blank=True, null=True, verbose_name="Contacto Recoleccion")
    fecha_hora_recoleccion = models.DateTimeField(null=True, blank=True, verbose_name="Fecha y Hora de Recolección")
    
    direccion_entrega = models.TextField(blank=True, null=True, verbose_name="Direccion Entrega")
    fecha_hora_entrega = models.DateTimeField(null=True, blank=True, verbose_name="Fecha y Hora de Entrega")
    contacto_entrega = models.TextField(blank=True, null=True, verbose_name="Contacto Entrega")
    
    es_nacional = models.BooleanField(default=True)

    completada = models.BooleanField(default=False)
    
    negocio = models.ForeignKey(Negocio, related_name='relRutasNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    creado_por = models.ForeignKey(User, related_name='relRutasCreateUser', on_delete=models.CASCADE, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, related_name='relRutasUpdateUser', on_delete=models.CASCADE, null=True, blank=True)

    def fn_calcular_monto_facturar_template(self):
        lv_monto_factura=0.00
        if self.kilometros_recorridos:
            objTarifa = AsignacionTarifa.objects.get(vehiculo=self.vehiculo, es_nacional = self.es_nacional)
            lv_monto_factura = objTarifa.precio_por_kilometro * self.kilometros_recorridos
        return "{0:.2f}".format(lv_monto_factura)
    
    def fn_calcular_monto_facturar(self):
        lv_monto_factura=0.00
        if self.kilometros_recorridos:
            objTarifa = AsignacionTarifa.objects.get(vehiculo=self.vehiculo, es_nacional = self.es_nacional)
            lv_monto_factura = objTarifa.precio_por_kilometro * self.kilometros_recorridos
        return lv_monto_factura
        

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id, vehiculo, piloto.
        """
        return '({}) - ({}) - ({})'.format(self.id, self.vehiculo, self.piloto)

    class Meta:
        verbose_name='Ruta'
        verbose_name_plural='Rutas'
        ordering = ['-id']


# Calcula los kilometros recorridos
@receiver(pre_save, sender=Rutas) 
def fn_calcular_kilometros_recorridos(sender, instance, **kwargs):
    
    if instance.kilometraje_entrada:
        instance.kilometros_recorridos = instance.kilometraje_entrada - instance.kilometraje_salida



# Reservar vehículo
@receiver(pre_save, sender=Rutas) 
def fn_reservar_vehiculo(sender, instance, **kwargs):
    
    if instance.vehiculo:
        if(instance.vehiculo.disponible is True):
            instance.vehiculo.disponible = False
            instance.vehiculo.save()


# Liberar vehículo
@receiver(pre_save, sender=Rutas) 
def fn_liberar_vehiculo(sender, instance, **kwargs):
    
    if(instance.completada):
        if instance.vehiculo:
            if(instance.vehiculo.disponible is False):
                instance.vehiculo.disponible = True
                instance.vehiculo.save()



class TipoLog(models.Model):
    """
    La clase TipoLog se utiliza para almacenar la lista de Tipos de Log para el seguimiento del transporte.

    Attributes:
        nombre_tipo_log : CharField
            Almacena el nombre del tipo de Log.

    Args:
        models (Model): Recibe como argumento Model de los modelos de Django.
    """
    nombre_tipo_log = models.CharField(max_length=150, blank=True, null=True, verbose_name="Nombre Tipo Log")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el nombre del tipo de log.
        """
        return '({}) {}'.format(self.id, self.nombre_tipo_log)

    class Meta:
        verbose_name='TipoLog'
        verbose_name_plural='Tipos Log'
        ordering = ['-id']





def elimina_imagen_cargada(instance, filename):
    """
    Función que eliminara físicamente alguna imagen que contenga el mismo nombre que el que se pasa como argumento.

    Args:
        instance (clase LogRuta): Instancia de la clase de que invoca.
        filename (str): Nombre de la ruta del archivo físico al que apunta la imagen.

    Returns:
        str: Devuelve la dirección física de la imagen
    """
    
    try:
        old_instance = LogRuta.objects.get(pk=instance.pk)
        old_instance.foto_seguimiento.delete()
    except:
        old_instance = None
    
    return 'log_rutas/' + filename


class LogRuta(ControlCreaciones):
    """
    La clase LogRuta se utiliza para almacenar los logs de la ruta.
    
    Attributes:
        ruta : ForeignKey
            Relación muchos a uno, Rutas con LogRuta.
        tipo_log : ForeignKey
            Relación muchos a uno, TipoLog con LogRuta.
        fecha_hora_log : DateTimeField
            Almacena la fecha y hora del log de la ruta.
        foto_seguimiento : ImageField
            Almacena la ruta para guardar documentos.
        observaciones : TextField
            Almacena las observaciones del log de la ruta.
        negocio : ForeignKey
            Relación muchos a uno, LogRuta con el Negocio.
        creado_por : ForeignKey
            Relación muchos a uno, LogRuta con Usuario que Creó.
        actualizado_por : ForeignKey
            Relación muchos a uno, LogRuta con Usuario que Actualizó.
    Args:
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    ruta = models.ForeignKey(Rutas, related_name='reLogRutaRutas', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Rutas")
    tipo_log = models.ForeignKey(TipoLog, related_name='relLogRutaTipoLog', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Tipo de Log")
    
    fecha_hora_log = models.DateTimeField(null=True, blank=True, verbose_name="Fecha y Hora del Log")
    foto_seguimiento = models.ImageField(upload_to=elimina_imagen_cargada, blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True, verbose_name="Observaciones")
    
    negocio = models.ForeignKey(Negocio, related_name='relLogRutaNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio")

    creado_por = models.ForeignKey(User, related_name='relLogRutaCreateUser', on_delete=models.CASCADE, null=True, blank=True)
    actualizado_por = models.ForeignKey(User, related_name='relLogRutaUpdateUser', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id, vehiculo, piloto.
        """
        return '({}) - ({}) - ({})'.format(self.id, self.ruta, self.tipo_log)

    class Meta:
        verbose_name='Log de Ruta'
        verbose_name_plural='Logs de Rutas'
        ordering = ['-id']







class FichaSalida(ControlCreaciones):
    """
    La clase FichaSalida se utiliza para almacenar las fichas de salida.
    
    Attributes:
        ruta : ForeignKey
            Relación muchos a uno, FichaSalida con Rutas.
        quien_entrega : ForeignKey
            Relación muchos a uno, FichaSalida con Empleado que Entrega.
        piloto : ForeignKey
            Relación muchos a uno, FichaSalida con Piloto/User.
        fecha_revision : DateField
            Almacena la fecha en la que se revisó el vehículo antes de salir del predio.
        kilometraje : CharField
            Almacena el kilometraje de salida.
        observacion_llantas : TextField
            Almacena las observaciones sobre el estado de las llantas.
        observacion_tapiceria : TextField
            Almacena las observaciones sobre el estado de la tapicería.
        observacion_carroceria : TextField
            Almacena las observaciones sobre el estado de la carrocería.
        observacion_combustible : TextField
            Almacena las observaciones sobre el estado del combustible.
    Args: 
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    ruta = models.ForeignKey(Rutas, related_name='reFichaSalidaRutas', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Ruta")
    quien_entrega = models.ForeignKey(User, related_name='relFichaSalidaEntregaUser', on_delete=models.CASCADE, null=True, blank=True)
    piloto = models.ForeignKey(User, related_name='relFichaSalidaPilotoUser', on_delete=models.CASCADE, null=True, blank=True)

    fecha_revision = models.DateField(null=True, blank=True, verbose_name="Fecha de Revisión")
    kilometraje = models.CharField(max_length=150, blank=True, null=True, verbose_name="Kilometraje")

    observacion_llantas = models.TextField(blank=True, null=True, verbose_name="Observación de Llantas")
    observacion_tapiceria = models.TextField(blank=True, null=True, verbose_name="Observación de Tapicería")
    observacion_carroceria = models.TextField(blank=True, null=True, verbose_name="Observación de Carrocería")
    observacion_combustible = models.TextField(blank=True, null=True, verbose_name="Observación de Combustible")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id, ruta, piloto.
        """
        return '({}) - ({}) - ({})'.format(self.id, self.ruta, self.piloto)

    class Meta:
        verbose_name='Ficha de Salida'
        verbose_name_plural='Fichas de Salida'
        ordering = ['-id']






class FichaEntrada(ControlCreaciones):
    """
    La clase FichaEntrada se utiliza para almacenar las fichas de salida.
    
    Attributes:
        ruta : ForeignKey
            Relación muchos a uno, FichaEntrada con Rutas.
        piloto : ForeignKey
            Relación muchos a uno, FichaEntrada con Piloto/User.
        quien_entrega : ForeignKey
            Relación muchos a uno, FichaEntrada con Empleado que Recibe.
        fecha_revision : DateField
            Almacena la fecha en la que se revisó el vehículo al regresar al predio.
        kilometraje : CharField
            Almacena el kilometraje de entrada.
        observacion_llantas : TextField
            Almacena las observaciones sobre el estado de las llantas.
        observacion_tapiceria : TextField
            Almacena las observaciones sobre el estado de la tapicería.
        observacion_carroceria : TextField
            Almacena las observaciones sobre el estado de la carrocería.
        observacion_combustible : TextField
            Almacena las observaciones sobre el estado del combustible.
    Args: 
        ControlCreaciones (clase abstracta): Hereda de la clase ControlCreaciones la cual almacena información de campos comúnes.
    """
    ruta = models.ForeignKey(Rutas, related_name='reFichaEntradaRutas', on_delete=models.CASCADE, null=True, blank=True, verbose_name="Ruta")
    piloto_entrega = models.ForeignKey(User, related_name='relFichaEntradaPilotoUser', on_delete=models.CASCADE, null=True, blank=True)
    quien_recibe = models.ForeignKey(User, related_name='relFichaEntradaEntregaUser', on_delete=models.CASCADE, null=True, blank=True)

    fecha_revision = models.DateField(null=True, blank=True, verbose_name="Fecha de Revisión")
    kilometraje = models.CharField(max_length=150, blank=True, null=True, verbose_name="Kilometraje")

    observacion_llantas = models.TextField(blank=True, null=True, verbose_name="Observación de Llantas")
    observacion_tapiceria = models.TextField(blank=True, null=True, verbose_name="Observación de Tapicería")
    observacion_carroceria = models.TextField(blank=True, null=True, verbose_name="Observación de Carrocería")
    observacion_combustible = models.TextField(blank=True, null=True, verbose_name="Observación de Combustible")
    observacion_general = models.TextField(blank=True, null=True, verbose_name="Observación General")

    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            string: Devuelve el id, ruta, piloto.
        """
        return '({}) - ({}) - ({})'.format(self.id, self.ruta, self.piloto)

    class Meta:
        verbose_name='Ficha de Entrada'
        verbose_name_plural='Fichas de Entrada'
        ordering = ['-id']

