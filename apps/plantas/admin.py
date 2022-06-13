from django.contrib import admin

from .models import Medidas, Producto, DetalleFactura, Inventario, IngresoCompras


admin.site.register(Medidas)
admin.site.register(Producto)
admin.site.register(DetalleFactura)
admin.site.register(Inventario)
admin.site.register(IngresoCompras)
