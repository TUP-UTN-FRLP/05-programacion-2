from django.db import models


class Cuenta(models.Model):
    numero = models.CharField(max_length=14, unique=True)
    titular = models.ManyToManyField('titulares.Titular',
                                     through='Titularidad',
                                     related_name="cuentas"
                                     )
    saldo = models.DecimalField(max_digits=12,
                                decimal_places=2,
                                default=0)
    activa = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'cuenta'
        verbose_name_plural = 'cuentas'
        ordering = ['numero']

    def __str__(self):
        return f'Cuenta {self.numero}'


class CuentaAhorro(Cuenta):
    tasa_interes_anual = models.DecimalField(max_digits=5,
                                             decimal_places=2,
                                             default=0)

    class Meta:
        verbose_name = 'cuenta de ahorro'
        verbose_name_plural = 'cuentas de ahorro'
        ordering = ['numero']

    def __str__(self):
        return f'Caja de ahorro {self.numero}'


class CuentaCorriente(Cuenta):
    limite_descubierto = models.DecimalField(max_digits=12,
                                             decimal_places=2,
                                             default=0)

    class Meta:
        verbose_name = 'cuenta corriente'
        verbose_name_plural = 'cuentas corrientes'
        ordering = ['numero']

    def __str__(self):
        return f'Cuenta corriente {self.numero}'


class Movimiento(models.Model):
    cuenta = models.ForeignKey(Cuenta,
                               on_delete=models.PROTECT,
                               related_name='movimientos')

    class Meta:
        verbose_name = 'movimiento'
        verbose_name_plural = 'movimientos'
        ordering = ['-id']

    def __str__(self):
        return f'Movimiento #{self.pk} - {self.cuenta}'


class Titularidad(models.Model):
    """Tabla intermedia explicita entre Cuenta y Titular."""
    cuenta = models.ForeignKey(Cuenta,
                               on_delete=models.PROTECT,
                               related_name='titularidades')
    titular = models.ForeignKey('titulares.Titular',
                                on_delete=models.PROTECT,
                                related_name='titularidades')
    fecha_alta = models.DateField(auto_now_add=True)
    es_principal = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'titularidad'
        verbose_name_plural = 'titularidades'
        constraints = [
            models.UniqueConstraint(fields=['cuenta', 'titular'],
                                    name='uniq_cuenta_titular'),
        ]

    def __str__(self):
        return f'{self.titular} - {self.cuenta}'
