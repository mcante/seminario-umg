from django.contrib import admin

from apps.planilla import models as m_planilla


admin.site.register(m_planilla.Puesto)
admin.site.register(m_planilla.Empleados)
admin.site.register(m_planilla.TipoPago)
admin.site.register(m_planilla.Meses)
admin.site.register(m_planilla.Planilla)
admin.site.register(m_planilla.EncabezadoPlanilla)
