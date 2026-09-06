# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# LSP, el caso clásico: en el capítulo 11 modelamos Cuadrado como hija
# de Rectangulo y quedó pendiente revisarlo. Agregale a Rectangulo los
# métodos cambiar_base() y cambiar_altura(), hacé que Cuadrado sincronice
# los dos lados y comprobá con assert que la sustitución falla. Después
# rehacé la jerarquía como clases hermanas.
# -------------------------------------------------------------------------

from abc import ABC, abstractmethod


class RectanguloMutable:
    """Promete que base y altura son independientes entre sí."""

    def __init__(self, base: float, altura: float) -> None:
        self._base = base
        self._altura = altura

    def cambiar_base(self, base: float) -> None:
        """Cambia solo la base."""
        self._base = base

    def cambiar_altura(self, altura: float) -> None:
        """Cambia solo la altura."""
        self._altura = altura

    def area(self) -> float:
        """Devuelve base por altura."""
        return self._base * self._altura


class CuadradoMalModelado(RectanguloMutable):
    """Hija que rompe la promesa del padre para seguir siendo cuadrado."""

    def __init__(self, lado: float) -> None:
        super().__init__(lado, lado)

    def cambiar_base(self, base: float) -> None:
        self._base = base
        self._altura = base

    def cambiar_altura(self, altura: float) -> None:
        self._base = altura
        self._altura = altura


def probar_contrato(rectangulo: RectanguloMutable) -> None:
    """Cliente que confía en el contrato de RectanguloMutable."""
    rectangulo.cambiar_base(5)
    rectangulo.cambiar_altura(3)

    assert rectangulo.area() == 15, (
        f"{type(rectangulo).__name__}: área {rectangulo.area()} "
        "en lugar de 15"
    )


# --- El modelo correcto: hermanas, no madre e hija ---

class Figura(ABC):
    """Base neutra que no promete lados independientes."""

    @abstractmethod
    def area(self) -> float:
        """Superficie encerrada por la figura."""


class Rectangulo(Figura):
    """Rectángulo con base y altura independientes."""

    def __init__(self, base: float, altura: float) -> None:
        self._base = base
        self._altura = altura

    def area(self) -> float:
        return self._base * self._altura


class Cuadrado(Figura):
    """Cuadrado definido por un único lado."""

    def __init__(self, lado: float) -> None:
        self._lado = lado

    def area(self) -> float:
        return self._lado ** 2


if __name__ == "__main__":
    probar_contrato(RectanguloMutable(1, 1))
    print("RectanguloMutable cumple su propio contrato")

    try:
        probar_contrato(CuadradoMalModelado(1))
    except AssertionError as error:
        print(f"LSP violado: {error}")

    # Con Rectangulo y Cuadrado como hermanas, nadie promete nada que
    # la otra no pueda cumplir: cada una solo sabe calcular su área.
    for figura in [Rectangulo(5, 3), Cuadrado(4)]:
        print(f"  {type(figura).__name__}: {figura.area()}")
