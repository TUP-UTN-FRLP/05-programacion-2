# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Diseñá una jerarquía MedioTransporte (ABC) con Bicicleta, Auto y
# Avion. Cada uno implementa tiempo_estimado(km) y costo(km). Después
# escribí mejor_opcion(km, medios), que reciba una lista de medios y
# devuelva el más rápido y el más económico. Anotá todo con type hints.
# -------------------------------------------------------------------------

from abc import ABC, abstractmethod


class MedioTransporte(ABC):
    """Contrato común para medios de transporte."""

    @abstractmethod
    def tiempo_estimado(self, km: float) -> float:
        """Horas estimadas para recorrer esos kilómetros."""

    @abstractmethod
    def costo(self, km: float) -> float:
        """Costo en pesos de recorrer esos kilómetros."""


class Bicicleta(MedioTransporte):
    """Bicicleta con velocidad media de 20 km/h."""

    def tiempo_estimado(self, km: float) -> float:
        return km / 20

    def costo(self, km: float) -> float:
        return 0.0


class Auto(MedioTransporte):
    """Auto con velocidad media de 80 km/h y costo por km."""

    def tiempo_estimado(self, km: float) -> float:
        return km / 80

    def costo(self, km: float) -> float:
        return km * 50


class Avion(MedioTransporte):
    """Avión con costo base más costo variable."""

    def tiempo_estimado(self, km: float) -> float:
        return km / 800

    def costo(self, km: float) -> float:
        return 100000 + km * 20


def mejor_opcion(
    km: float,
    medios: list[MedioTransporte],
) -> tuple[MedioTransporte, MedioTransporte]:
    """Devuelve el medio más rápido y el más económico."""
    mas_rapido = min(
        medios,
        key=lambda medio: medio.tiempo_estimado(km),
    )
    mas_barato = min(
        medios,
        key=lambda medio: medio.costo(km),
    )

    return mas_rapido, mas_barato


if __name__ == "__main__":
    rapido, barato = mejor_opcion(
        500,
        [Bicicleta(), Auto(), Avion()],
    )

    print(f"Más rápido: {type(rapido).__name__}")
    print(f"Más barato: {type(barato).__name__}")
