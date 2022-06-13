from django.db.models import Avg, Max, Sum, Min, Count
from django.db.models import Q
from apps.factura.models import Pedido
import datetime
from django.utils import timezone
from apps.registration.models import Perfil, NegocioUsuario
from apps.clientes.models import Contacto
from apps.mensajeria.models import EncabezadoMensaje, HiloMensaje
from apps.transportes import models as m_transportes


# Procesador de contexto.
def notificaciones(request):
    if request.user.is_authenticated: # Validar si hay usuario autenticado para hacer las consultas y evitar generar errores, sino hay entonces que retorne una lista vacía.
        
        p_negocio=request.user.relPerfilUsuario.negocio
        
        objRutasAlertadas = None
        try:
            objRuta = m_transportes.Rutas.objects.filter(completada=False)
            #print(objRuta.all().values('vehiculo__dispositivo_gps'))
            objRutaFechas = m_transportes.Rutas.objects.filter(completada=False).aggregate(Min("fecha_salida_predio"), Max("fecha_entrada_predio"))
            new_end = objRutaFechas['fecha_entrada_predio__max'] + datetime.timedelta(days=1) # a la última fecha hay que sumarle 1 día porque django ignora los datetime del último día para un rango: https://ajaxhispano.com/ask/django-database-query-como-filtrar-objetos-por-rango-de-fechas-4084/
            velAlertada = m_transportes.LogVelocidadesGPS.objects.filter(dispositivo_gps__in=(objRuta.all().values('vehiculo__dispositivo_gps')), creado__range = [objRutaFechas['fecha_salida_predio__min'], new_end], velocidad_alertada=True).values_list('dispositivo_gps')

            objRutasAlertadas = objRuta.filter(vehiculo__dispositivo_gps__in=velAlertada.all().distinct())
            #print(velAlertada)
            #print(objRutasAlertadas)
        except Exception as e:
            print('Error processor: {}'.format(e))

        # Mostrar los mensajes que sean para el negocio activo
        ObjHiloMensaje = HiloMensaje.objects.filter(negocio_destino = p_negocio, mensaje_leido=False)

        ObjContacto = Contacto.objects.filter(negocio=p_negocio, atentido=False)

        ObjPedido = Pedido.objects.filter(cliente__relNegocioClienteCliente__vendedor=request.user, completado=False).distinct()
        #print(ObjPedido.count())

        ObjCantidadNegocios = NegocioUsuario.objects.filter(perfil_usuario__user=request.user).count()
        #print(ObjCantidadNegocios)
        # Saldias de Notificaciones

        #import pdb; pdb.set_trace()

        NOTIFICACIONES = {  
                            'ObjPedidos':ObjPedido,
                            'ObjNegociosUsuario':ObjCantidadNegocios,
                            'ObjContactos':ObjContacto,
                            'ObjHiloMensaje':ObjHiloMensaje,
                            'objRutasAlertadas': objRutasAlertadas,
                        } # Generar una lista de cada consulta y devolverlas para ser utilizadas en cualquier template.
    else:
        return {}
    return NOTIFICACIONES

