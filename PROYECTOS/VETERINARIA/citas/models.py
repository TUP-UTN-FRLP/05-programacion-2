from django.db import models


class Cita(models.Model):
    class Estado(models.TextChoices):
        PENDIENTE = 'pendiente', 'Pendiente'
        CONFIRMADA = 'confirmada', 'Confirmada'
        ATENDIDA = 'atendida', 'Atendida'
        CANCELADA = 'cancelada', 'Cancelada'

    mascota = models.ForeignKey(
        'mascotas.Mascota', on_delete=models.CASCADE, related_name='citas'
    )
    fecha_hora = models.DateTimeField()
    motivo = models.CharField(max_length=200)
    estado = models.CharField(
        max_length=20, choices=Estado.choices, default=Estado.PENDIENTE
    )
    notas = models.TextField(blank=True)

    class Meta:
        ordering = ['fecha_hora']

    def __str__(self):
        return f'{self.mascota.nombre} - {self.fecha_hora:%d/%m/%Y %H:%M}'
