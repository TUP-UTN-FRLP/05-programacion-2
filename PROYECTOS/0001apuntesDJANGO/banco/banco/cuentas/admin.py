from django.contrib import admin

from .models import (Cuenta, CuentaAhorro, CuentaCorriente, Movimiento,
                     Titularidad)


class TitularidadInline(admin.TabularInline):
    model = Titularidad
    extra = 1
    autocomplete_fields = ['titular']   # buscador por nombre / DNI / CUIT
    readonly_fields = ['fecha_alta']


class CuentaAdmin(admin.ModelAdmin):
    inlines = [TitularidadInline]


admin.site.register(Cuenta, CuentaAdmin)
admin.site.register(CuentaAhorro, CuentaAdmin)
admin.site.register(CuentaCorriente, CuentaAdmin)
admin.site.register(Movimiento)
admin.site.register(Titularidad)
