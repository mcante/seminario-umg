"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include # include, permite llamar a un conjunto de urls
from django.conf import settings # Importar la configuracion de django
from rest_framework.authtoken import views

from django.conf.urls import handler404, handler500
from apps.clientes.views import Error400TemplateView, Error505TemplateView


##las vistas creadas
handler404 = Error400TemplateView.as_view()
handler500 = Error505TemplateView.as_error_view()


urlpatterns = [
    path('admin/', admin.site.urls),


    # Mis URLs
    path('perfil/', include('apps.registration.urls')),
    
    path('', include('apps.clientes.urls')),
    path('factura/', include('apps.factura.urls')),
    path('gastos/', include('apps.gastos.urls')),
    path('plantas/', include('apps.plantas.urls')),
    path('proyectos/', include('apps.proyectos.urls')),
    path('transportes/', include('apps.transportes.urls')),
    path('maquinarias/', include('apps.ventas_y_alquileres.urls')),
    path('planilla/', include('apps.planilla.urls')),
    path('mensajeria/', include('apps.mensajeria.urls')),
    

    # LOGIN ADMIN
    path('accounts/', include('django.contrib.auth.urls')),

    # Retorna tokens de authenticacion para REST API
    path('api-token-auth/',views.obtain_auth_token,name='api-token-auth'),

    #path('__debug__/', include('debug_toolbar.urls')),
]

# Cambiar el texto de la consola de administración
admin.site.site_header = 'Administración de TransPort'

if settings.DEBUG:
    from django.conf.urls.static import static
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
