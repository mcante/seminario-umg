from django.db import models

from django.contrib.auth.models import User
from apps.registration.models import Negocio
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



class EncabezadoMensaje(ControlCreaciones):
    enviado_por = models.ForeignKey(User, related_name='relEncabezadoMensajeUser', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Enviado Por")
    mensaje = models.TextField(blank=True, null=True, verbose_name="Mensaje")
    finalizar_conversacion = models.BooleanField(default=False)
    negocio_origen = models.ForeignKey(Negocio, related_name='relEncabezadoMensajeOrigenNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio Origen")
    negocio_destino = models.ForeignKey(Negocio, related_name='relEncabezadoMensajeDestinoNegocio', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio Destino")
    
    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            str: Devuelve el nombre nombre completo del usuario.
        """
        return '({}) {} {} => {}'.format(self.id, self.enviado_por.get_full_name(), self.negocio_origen, self.negocio_destino)

    class Meta:
        verbose_name='Encabezado de Mensaje'
        verbose_name_plural='Encabezado de Mensajes'
        ordering = ['-id']
    


class HiloMensaje(ControlCreaciones):
    encabezado_mensaje = models.ForeignKey(EncabezadoMensaje, related_name='relHiloMensajeEncabezadoMensaje', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Encabezado")    
    mensaje = models.TextField(blank=True, null=True, verbose_name="Mensaje")
    mensaje_leido = models.BooleanField(default=False, verbose_name="Marcar como Mensaje Leído")

    negocio_origen = models.ForeignKey(Negocio, related_name='relHiloMensajeNegocioOrigen', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio Origen")
    negocio_destino = models.ForeignKey(Negocio, related_name='relHiloMensajeNegocioDestino', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Negocio Destino")
    enviado_por = models.ForeignKey(User, related_name='relHiloMensajejeUser', on_delete=models.CASCADE, blank=True, null=True, verbose_name="Enviado Por")
    
    def __str__(self):
        """
        Función para mostrar un campo o campos cada vez que se consulte la clase.

        Returns:
            str: Devuelve el nombre nombre completo del usuario.
        """
        return '({}) {} {}'.format(self.id, self.encabezado_mensaje, self.mensaje_leido)

    class Meta:
        verbose_name='Hilo de Mensaje'
        verbose_name_plural='Hilo de Mensajes'
        ordering = ['-id']
    





@receiver(post_save, sender=EncabezadoMensaje)
def fn_asigna_negocio_destino(sender, instance, **kwargs):
    """
    Función agrega el primer mensaje del encabezado al hilo.

    Args:
        sender (clase EncabezadoMensaje): Clase EncabezadoMensaje que invoca la función signal.
        instance (instancia de la clase): Objecto o instancia que ejecutó al signal.
    """

    # VALIDA SI SE CREO
    if kwargs.get('created', True):


        HiloMensaje.objects.create(
            encabezado_mensaje = instance,
            mensaje = instance.mensaje,
            negocio_origen = instance.negocio_origen,
            negocio_destino = instance.negocio_destino,
            enviado_por = instance.enviado_por
        )




@receiver(pre_save, sender=HiloMensaje)
def fn_asigna_negocio_destino(sender, instance, **kwargs):
    """
    Función encuentra el negocio destino y lo asigna.

    Args:
        sender (clase HiloMensaje): Clase HiloMensaje que invoca la función signal.
        instance (instancia de la clase): Objecto o instancia que ejecutó al signal.
    """

    # VALIDA SI SE CREO
    if kwargs.get('created', True):
        # cargar los dos negocios del encabezado
        p_negocio_uno = instance.encabezado_mensaje.negocio_origen
        p_negocio_dos = instance.encabezado_mensaje.negocio_destino

        # El negocio de origen debe de ser distinto al destino
        lv_negocio = None
        if(p_negocio_uno == instance.negocio_origen):
            lv_negocio = p_negocio_dos
        else:
            lv_negocio = p_negocio_uno

        instance.negocio_destino = lv_negocio
        



