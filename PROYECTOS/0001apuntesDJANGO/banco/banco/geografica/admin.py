from django.contrib import admin

from .models import Provincia, Departamento, Localidad

admin.site.register(Provincia)
admin.site.register(Departamento)
admin.site.register(Localidad)
