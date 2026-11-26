# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# El siguiente código viola OCP: area_figura() distingue por tipo entre
# circulo, cuadrado y rectangulo para calcular el área. Reescribilo con
# herencia y polimorfismo, y después agregá Triangulo sin tocar nada de
# lo anterior.
# -------------------------------------------------------------------------

import math
from abc import ABC, abstractmethod


class Figura(ABC):
    """Figura cuyo cálculo de área implementa cada hija."""

    @abstractmethod
    def area(self):
        """Superficie encerrada por la figura."""


class Circulo(Figura):
    """Círculo definido por su radio."""

    def __init__(self, radio):
        self._radio = radio

    def area(self):
        return math.pi * self._radio ** 2


class Cuadrado(Figura):
    """Cuadrado definido por su lado."""

    def __init__(self, lado):
        self._lado = lado

    def area(self):
        return self._lado ** 2


class Rectangulo(Figura):
    """Rectángulo definido por base y altura."""

    def __init__(self, base, altura):
        self._base = base
        self._altura = altura

    def area(self):
        return self._base * self._altura


class Triangulo(Figura):
    """Figura agregada después: ninguna clase anterior cambió."""

    def __init__(self, base, altura):
        self._base = base
        self._altura = altura

    def area(self):
        return self._base * self._altura / 2


if __name__ == "__main__":
    figuras = [Circulo(5), Cuadrado(3), Rectangulo(4, 6), Triangulo(6, 4)]

    for figura in figuras:
        print(f"  {type(figura).__name__}: {figura.area():.2f}")
