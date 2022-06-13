from django.contrib import admin

from .models import Cliente, Telefonos, NegocioCliente, Contacto


class NegocioClienteInline(admin.TabularInline):
    model = NegocioCliente
    extra = 0
    autocomplete_fields = ['cliente']

class TelefonosInline(admin.TabularInline):
    model = Telefonos
    extra = 0
    autocomplete_fields = ['cliente']

class ClienteAdmin(admin.ModelAdmin):
    inlines = [NegocioClienteInline, TelefonosInline,]
    list_display = (
        'nombre_empresa',
        'nombre_contacto',
        'telefono',
        'nit',
        'NombreEmpleado',
        'id',
    )
    #
    def NombreEmpleado(self, obj):
        lv_nombreEmpleado = ''
        try:
            lv_nombreEmpleado = obj.empleado_asignado.first_name + ' ' + obj.empleado_asignado.last_name
        except:
            lv_nombreEmpleado = '---'
        return lv_nombreEmpleado
    #
    search_fields = ('nombre_empresa', 'nombre_contacto',)
    list_filter = ('nit',)


admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Telefonos)
admin.site.register(NegocioCliente)
admin.site.register(Contacto)
