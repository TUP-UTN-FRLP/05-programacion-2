# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Continuando el ejercicio 4, creá una lista con figuras mixtas y
# calculá el área total sumando area() de cada una. El código que suma
# no debe preguntar de qué tipo es cada figura: eso es polimorfismo.
# -------------------------------------------------------------------------

class Figura:
    """Figura base cuyo cálculo de área debe implementar cada hija."""

    def area(self):
        """Contrato que toda figura concreta debe cumplir."""
        raise NotImplementedError(
            f"La clase {type(self).__name__} debe implementar area()"
        )


class Cuadrado(Figura):
    """Cuadrado definido por su lado."""

    def __init__(self, lado):
        self._lado = lado

    def area(self):
        """Devuelve lado al cuadrado."""
        return self._lado ** 2


class Rectangulo(Figura):
    """Rectángulo definido por base y altura."""

    def __init__(self, base, altura):
        self._base = base
        self._altura = altura

    def area(self):
        """Devuelve base por altura."""
        return self._base * self._altura


class Triangulo(Figura):
    """Triángulo definido por base y altura."""

    def __init__(self, base, altura):
        self._base = base
        self._altura = altura

    def area(self):
        """Devuelve base por altura sobre dos."""
        return self._base * self._altura / 2


figuras = [
    Cuadrado(4),
    Rectangulo(5, 3),
    Triangulo(6, 4),
]

total = sum(figura.area() for figura in figuras)
print(f"Área total: {total}")
