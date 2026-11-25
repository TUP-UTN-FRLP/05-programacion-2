from django.contrib import admin

from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = ('apellido', 'nombre', 'telefono', 'email')
    search_fields = ('apellido', 'nombre', 'telefono', 'email')
