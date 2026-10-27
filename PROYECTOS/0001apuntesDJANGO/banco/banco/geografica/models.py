from django.db import models


class Provincia(models.Model):
    codigo_georef = models.CharField(max_length=2, unique=True)
    categoria = models.CharField(max_length=100, blank=True)
    nombre = models.CharField(max_length=100)

    class Meta:
        verbose_name = 'provincia'
        verbose_name_plural = 'provincias'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


class Departamento(models.Model):
    codigo_georef = models.CharField(max_length=20, unique=True)
    categoria = models.CharField(max_length=100, blank=True)
    nombre = models.CharField(max_length=100)
    provincia = models.ForeignKey(Provincia, on_delete=models.PROTECT)

    class Meta:
        verbose_name = 'departamento'
        verbose_name_plural = 'departamentos'
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} ({self.provincia})'


class Localidad(models.Model):
    codigo_georef = models.CharField(max_length=20, unique=True)
    categoria = models.CharField(max_length=100, blank=True)
    nombre = models.CharField(max_length=100)
    localidad = models.ForeignKey(Departamento,
                                  on_delete=models.PROTECT,
                                  related_name='localidades'
                                  )

    class Meta:
        verbose_name = 'localidad'
        verbose_name_plural = 'localidades'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
