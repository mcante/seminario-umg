from django.contrib import admin

from .models import Marca, TipoMaquina, Maquina, InventarioMaquinariaVentas, IngresoCompras, \
InventarioMaquinariaAlquiler, EstadoAlquiler, AlquilerMaquina, DetalleFactura



admin.site.register(Marca)
admin.site.register(TipoMaquina)
admin.site.register(Maquina)

admin.site.register(IngresoCompras)
admin.site.register(InventarioMaquinariaVentas)

admin.site.register(InventarioMaquinariaAlquiler)

admin.site.register(EstadoAlquiler)
admin.site.register(AlquilerMaquina)
admin.site.register(DetalleFactura)
