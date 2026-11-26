# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ABC y polimorfismo: hacé una jerarquía Forma (ABC) con area() y
# perimetro() abstractos, y las clases Circulo, Rectangulo y Triangulo.
# Después escribí forma_con_mayor_area(formas), que devuelva la forma de
# mayor área sin preguntar de qué tipo es ninguna.
# -------------------------------------------------------------------------

import math
from abc import ABC, abstractmethod


class Forma(ABC):
    """Forma abstracta con área y perímetro."""

    @abstractmethod
    def area(self) -> float:
        """Superficie encerrada por la forma."""

    @abstractmethod
    def perimetro(self) -> float:
        """Longitud del contorno de la forma."""

    def __str__(self) -> str:
        return (
            f"{type(self).__name__}: área {self.area():.2f}, "
            f"perímetro {self.perimetro():.2f}"
        )


class Circulo(Forma):
    """Círculo definido por su radio."""

    def __init__(self, radio: float) -> None:
        self._radio = radio

    def area(self) -> float:
        return math.pi * self._radio ** 2

    def perimetro(self) -> float:
        return 2 * math.pi * self._radio


class Rectangulo(Forma):
    """Rectángulo definido por base y altura."""

    def __init__(self, base: float, altura: float) -> None:
        self._base = base
        self._altura = altura

    def area(self) -> float:
        return self._base * self._altura

    def perimetro(self) -> float:
        return 2 * (self._base + self._altura)


class Triangulo(Forma):
    """Triángulo definido por sus tres lados."""

    def __init__(self, lado_a: float, lado_b: float,
                 lado_c: float) -> None:
        self._lado_a = lado_a
        self._lado_b = lado_b
        self._lado_c = lado_c

    def area(self) -> float:
        """Área por la fórmula de Herón."""
        semi = self.perimetro() / 2
        return math.sqrt(
            semi
            * (semi - self._lado_a)
            * (semi - self._lado_b)
            * (semi - self._lado_c)
        )

    def perimetro(self) -> float:
        return self._lado_a + self._lado_b + self._lado_c


def forma_con_mayor_area(formas: list[Forma]) -> Forma:
    """Devuelve la forma de mayor área de la lista."""
    return max(formas, key=lambda forma: forma.area())


if __name__ == "__main__":
    formas = [Circulo(5), Rectangulo(4, 6), Triangulo(3, 4, 5)]

    for forma in formas:
        print(forma)

    mejor = forma_con_mayor_area(formas)
    print(f"Mayor área: {type(mejor).__name__}")
