# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Convertí Vehiculo en una clase abstracta con ABC y un método
# abstracto costo_operativo_mensual(). Hacé tres hijas concretas: Auto,
# Camion y Moto, cada una con su propia fórmula. Verificá que no podés
# instanciar Vehiculo directamente y que una hija incompleta tampoco.
# -------------------------------------------------------------------------

from abc import ABC, abstractmethod


class Vehiculo(ABC):
    """Vehículo abstracto con un costo operativo mensual."""

    def __init__(self, marca):
        self._marca = marca

    def marca(self):
        """Devuelve la marca del vehículo."""
        return self._marca

    @abstractmethod
    def costo_operativo_mensual(self):
        """Costo mensual de operar el vehículo, en pesos."""

    def __str__(self):
        return (
            f"{type(self).__name__} {self._marca}: "
            f"${self.costo_operativo_mensual()}/mes"
        )


class Auto(Vehiculo):
    """Auto con costo operativo fijo."""

    def costo_operativo_mensual(self):
        return 50000


class Camion(Vehiculo):
    """Camión con costo operativo fijo."""

    def costo_operativo_mensual(self):
        return 200000


class Moto(Vehiculo):
    """Moto con costo operativo fijo."""

    def costo_operativo_mensual(self):
        return 15000


class Tractor(Vehiculo):
    """Hija incompleta: no implementa el método abstracto."""


if __name__ == "__main__":
    for vehiculo in [Auto("Ford"), Camion("Scania"), Moto("Honda")]:
        print(vehiculo)

    try:
        Vehiculo("cualquiera")
    except TypeError as error:
        print(f"Vehiculo es abstracta: {error}")

    try:
        Tractor("John Deere")
    except TypeError as error:
        print(f"Tractor quedó incompleta: {error}")
