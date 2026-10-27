from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class Titular(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(blank=True)
    telefono = models.CharField(max_length=30, blank=True)

    class Meta:
        verbose_name = 'titular'
        verbose_name_plural = 'titulares'
        ordering = ['nombre']

    def __str__(self):
        # Si el titular es persona fisica o juridica, muestra el detalle con
        # DNI o CUIT (asi se ve en el buscador del admin y en los desplegables).
        for relacion in ('personafisica', 'personajuridica'):
            try:
                return str(getattr(self, relacion))
            except ObjectDoesNotExist:
                continue
        return self.nombre


class PersonaFisica(Titular):
    apellido = models.CharField(max_length=100)
    dni = models.CharField(max_length=8, unique=True)
    edad = models.IntegerField()

    class Meta:
        verbose_name = 'persona física'
        verbose_name_plural = 'personas físicas'
        ordering = ['apellido', 'nombre']

    def __str__(self):
        return f'{self.apellido}, {self.nombre} (DNI {self.dni})'


class PersonaJuridica(Titular):
    cuit = models.CharField(max_length=11, unique=True)

    class Meta:
        verbose_name = 'persona jurídica'
        verbose_name_plural = 'personas jurídicas'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} (CUIT {self.cuit})'


class Domicilio(models.Model):
    titular = models.OneToOneField('titulares.Titular',
                                   on_delete=models.CASCADE,
                                   related_name="domicilio"
                                   )
    localidad = models.ForeignKey('geografica.Localidad',
                                  on_delete=models.PROTECT,
                                  related_name='domicilios'
                                  )
    calle = models.CharField(max_length=150)
    altura = models.CharField(max_length=10)
    piso = models.CharField(max_length=10, blank=True)
    departamento = models.CharField(max_length=10, blank=True)

    class Meta:
        verbose_name = 'domicilio'
        verbose_name_plural = 'domicilios'

    def __str__(self):
        direccion = f'{self.calle} {self.altura}'
        if self.piso:
            direccion += f', piso {self.piso}'
        if self.departamento:
            direccion += f', depto. {self.departamento}'
        return f'{direccion} - {self.localidad}'
