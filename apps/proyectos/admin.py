from django.contrib import admin

from .models import TipoProyecto, Proyecto, Documentos, GastosProyecto, DetalleFacturaEntregables


admin.site.register(TipoProyecto)
admin.site.register(Proyecto)
admin.site.register(Documentos)
admin.site.register(GastosProyecto)
admin.site.register(DetalleFacturaEntregables)
