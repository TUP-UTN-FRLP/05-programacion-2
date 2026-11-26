from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import FormularioAltaUsuario, FormularioCambioAdministrador
from .models import Usuario


@admin.register(Usuario)
class AdministradorUsuario(UserAdmin):
    add_form = FormularioAltaUsuario
    form = FormularioCambioAdministrador
    model = Usuario
    list_display = ('email', 'apellido', 'nombre', 'dni', 'is_active', 'is_staff')
    ordering = ()

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Datos personales', {'fields': ('nombre', 'apellido', 'dni', 'telefono', 'fecha_nacimiento')}),
        ('Roles y permisos', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Fechas', {'fields': ('last_login', 'date_joined', 'creado_en', 'actualizado_en')}),
    )
    readonly_fields = ('creado_en', 'actualizado_en')
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email', 'nombre', 'apellido', 'dni', 'telefono',
                'fecha_nacimiento', 'rol', 'is_active', 'contrasena',
                'confirmar_contrasena',
            ),
        }),
    )
