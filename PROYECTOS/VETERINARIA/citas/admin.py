from django.contrib import admin

from .models import Cita


@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    list_display = ('fecha_hora', 'mascota', 'motivo', 'estado')
    list_filter = ('estado',)
    date_hierarchy = 'fecha_hora'
    search_fields = ('mascota__nombre', 'motivo')
