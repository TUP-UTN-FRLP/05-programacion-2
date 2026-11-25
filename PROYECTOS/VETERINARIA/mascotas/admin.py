from django.contrib import admin

from .models import Mascota


@admin.register(Mascota)
class MascotaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'especie', 'raza', 'cliente')
    list_filter = ('especie',)
    search_fields = ('nombre', 'cliente__apellido', 'cliente__nombre')
