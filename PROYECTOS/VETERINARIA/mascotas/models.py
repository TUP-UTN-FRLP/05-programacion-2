from django.db import models


class Mascota(models.Model):
    class Especie(models.TextChoices):
        PERRO = 'perro', 'Perro'
        GATO = 'gato', 'Gato'
        AVE = 'ave', 'Ave'
        OTRO = 'otro', 'Otro'

    cliente = models.ForeignKey(
        'clientes.Cliente', on_delete=models.CASCADE, related_name='mascotas'
    )
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=20, choices=Especie.choices)
    raza = models.CharField(max_length=100, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['nombre']

    def __str__(self):
        return f'{self.nombre} ({self.get_especie_display()})'
