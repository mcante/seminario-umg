from django.contrib import admin

from .models import EstadoFactura, TipoPago, EstadoVenta, CorrelativoFactura, Factura, \
Ventas, \
EstadoPedido, Pedido, \
EstadoDespacho, Despacho

#Factura
admin.site.register(EstadoFactura)
admin.site.register(TipoPago)
admin.site.register(EstadoVenta)
admin.site.register(CorrelativoFactura)
admin.site.register(Factura)
#Ventas
admin.site.register(Ventas)
#Pedidos
admin.site.register(EstadoPedido)
admin.site.register(Pedido)
#Despachos
admin.site.register(EstadoDespacho)
admin.site.register(Despacho)