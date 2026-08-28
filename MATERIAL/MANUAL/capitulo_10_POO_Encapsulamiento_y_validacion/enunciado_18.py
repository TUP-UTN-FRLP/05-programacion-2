# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Creá una excepción LimiteExtraccionSuperadoError. Hacé una clase
# Cajero con un _limite_diario privado (por defecto 100000) y un método
# extraer(monto) que rechace si monto > limite_diario.
# -------------------------------------------------------------------------


class LimiteExtraccionSuperadoError(Exception):
    pass


class Cajero:
    def __init__(self, limite_diario=100000):
        if limite_diario <= 0:
            raise ValueError("El límite debe ser positivo")

        self._limite_diario = limite_diario

    @property
    def limite_diario(self):
        return self._limite_diario

    def extraer(self, monto):
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")

        if monto > self._limite_diario:
            raise LimiteExtraccionSuperadoError(
                f"El límite diario es ${self._limite_diario}"
            )

        print(f"Extrayendo ${monto}...")


c = Cajero()

c.extraer(50000)  # OK

c.extraer(200000)  # LimiteExtraccionSuperadoError
