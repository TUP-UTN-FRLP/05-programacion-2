from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class AdministradorDeUsuarios(BaseUserManager):
    """Crea usuarios cuya identificación para ingresar es el email."""

    def crear_usuario(self, email, contrasena=None, **campos_adicionales):
        if not email:
            raise ValueError('El email es obligatorio.')

        email = self.normalize_email(email)
        usuario = self.model(email=email, **campos_adicionales)
        usuario.set_password(contrasena)
        usuario.save(using=self._db)
        return usuario

    # Estos nombres son requeridos por Django para sus comandos y el admin.
    def create_user(self, email, password=None, **campos_adicionales):
        campos_adicionales.setdefault('is_staff', False)
        campos_adicionales.setdefault('is_superuser', False)
        return self.crear_usuario(email, password, **campos_adicionales)

    def create_superuser(self, email, password=None, **campos_adicionales):
        campos_adicionales.setdefault('is_staff', True)
        campos_adicionales.setdefault('is_superuser', True)
        campos_adicionales.setdefault('is_active', True)

        if campos_adicionales.get('is_staff') is not True:
            raise ValueError('El superusuario debe tener is_staff=True.')
        if campos_adicionales.get('is_superuser') is not True:
            raise ValueError('El superusuario debe tener is_superuser=True.')
        return self.crear_usuario(email, password, **campos_adicionales)


class Usuario(AbstractUser):
    """Cuenta de acceso y datos personales de una persona registrada."""

    username = None

    nombre = models.CharField(max_length=60)
    apellido = models.CharField(max_length=60)
    dni = models.CharField('DNI', max_length=8, unique=True)
    telefono = models.CharField(max_length=30, unique=True)
    email = models.EmailField('Correo electrónico', unique=True)
    fecha_nacimiento = models.DateField()
    is_active = models.BooleanField('Usuario activo', default=True)
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    objects = AdministradorDeUsuarios()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ('nombre', 'apellido', 'dni', 'telefono', 'fecha_nacimiento')

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'

    def __str__(self):
        return f'{self.apellido}, {self.nombre} ({self.email})'
