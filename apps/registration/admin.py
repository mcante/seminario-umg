from django.contrib import admin
from .models import Departamento, Negocio, TipoEmpleado, Perfil, GiroNegocio, NegocioUsuario, Pais, Municipio, Presupuesto
from django.contrib.auth.models import User, Permission
from django.contrib.contenttypes.models import ContentType




class NegocioUsuarioInline(admin.TabularInline):
    model = NegocioUsuario
    extra = 0
    autocomplete_fields = ['perfil_usuario']


class PerfilAdmin(admin.ModelAdmin):
    inlines = [NegocioUsuarioInline,]
    list_display = (
        'NombreCompleto',
        'user',
        'celular',
        'negocio',
        'id',
    )
    #
    def NombreCompleto(self, obj):
        return obj.user.first_name + ' ' + obj.user.last_name
    #
    search_fields = ('user__username', 'negocio__nombre_negocio',)
    list_filter = ('negocio',)
    
    #
    #filter_horizontal = ['accesos_cas',]


admin.site.register(Pais)
admin.site.register(Departamento)
admin.site.register(Municipio)
admin.site.register(Negocio)
admin.site.register(TipoEmpleado)
admin.site.register(Perfil, PerfilAdmin)
admin.site.register(GiroNegocio)
admin.site.register(NegocioUsuario)
admin.site.register(Presupuesto)

admin.site.register(Permission)
admin.site.register(ContentType)

