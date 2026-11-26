# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Verificá OCP con assert. Partí de la jerarquía Forma del ejercicio 10
# y de una función area_total(formas) ya escrita. Agregá un Pentagono
# regular y comprobá que area_total sigue funcionando sin haber sido
# modificada. Mostrá también que el código fuente de la función es el
# mismo antes y después.
# -------------------------------------------------------------------------

import inspect
import math
from abc import ABC, abstractmethod


class Forma(ABC):
    """Forma abstracta con cálculo de área."""

    @abstractmethod
    def area(self) -> float:
        """Superficie encerrada por la forma."""


class Circulo(Forma):
    """Círculo definido por su radio."""

    def __init__(self, radio: float) -> None:
        self._radio = radio

    def area(self) -> float:
        return math.pi * self._radio ** 2


class Rectangulo(Forma):
    """Rectángulo definido por base y altura."""

    def __init__(self, base: float, altura: float) -> None:
        self._base = base
        self._altura = altura

    def area(self) -> float:
        return self._base * self._altura


def area_total(formas: list[Forma]) -> float:
    """Suma áreas sin conocer los tipos concretos."""
    return sum(forma.area() for forma in formas)


class Pentagono(Forma):
    """Forma agregada después, sin tocar area_total."""

    def __init__(self, lado: float) -> None:
        self._lado = lado

    def area(self) -> float:
        numerador = 5 * self._lado ** 2
        denominador = 4 * math.tan(math.pi / 5)
        return numerador / denominador


def probar_ocp() -> None:
    """Verifica que la forma nueva no obligó a cambiar area_total."""
    codigo_antes = inspect.getsource(area_total)

    originales = [Circulo(5), Rectangulo(4, 6)]
    total_original = area_total(originales)

    extendidas = originales + [Pentagono(3)]
    total_nuevo = area_total(extendidas)

    assert total_nuevo > total_original, (
        "el total con la forma nueva debería ser mayor"
    )

    codigo_despues = inspect.getsource(area_total)
    assert codigo_antes == codigo_despues, (
        "area_total no debería haber cambiado"
    )

    print(f"Total original: {total_original:.2f}")
    print(f"Total con Pentagono: {total_nuevo:.2f}")
    print("OCP verificado: area_total quedó intacta")


if __name__ == "__main__":
    probar_ocp()
