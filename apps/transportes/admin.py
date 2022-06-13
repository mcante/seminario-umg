from django.contrib import admin

from .models import Marca, Linea, TipoVehiculo, TransmisionVehiculo, \
DispositivoGPS, LogVelocidadesGPS, LogTiemposGPS, \
InventarioVehiculo, AsignacionTarifa, \
Rutas, TipoLog, LogRuta, FichaSalida, FichaEntrada

admin.site.register(Marca)
admin.site.register(Linea)
admin.site.register(TipoVehiculo)
admin.site.register(TransmisionVehiculo)

admin.site.register(DispositivoGPS)
admin.site.register(LogVelocidadesGPS)
admin.site.register(LogTiemposGPS)

admin.site.register(InventarioVehiculo)
admin.site.register(AsignacionTarifa)

admin.site.register(Rutas)
admin.site.register(TipoLog)
admin.site.register(LogRuta)
admin.site.register(FichaSalida)
admin.site.register(FichaEntrada)
