from django.contrib import admin

from apps.mensajeria import models as m_mensajeria

#Mensajería
admin.site.register(m_mensajeria.EncabezadoMensaje)
admin.site.register(m_mensajeria.HiloMensaje)
