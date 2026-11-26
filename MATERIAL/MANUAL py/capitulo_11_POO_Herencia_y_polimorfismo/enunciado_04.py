# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Figura con un método abstracto conceptual area(), que
# lanza NotImplementedError informando el nombre de la clase concreta.
# Definí tres hijas: Cuadrado(lado), Rectangulo(base, altura) y
# Triangulo(base, altura). Cada una implementa area(). Comprobá también
# qué pasa si alguien instancia Figura y le pide el área.
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


print(Cuadrado(4).area())
print(Rectangulo(5, 3).area())
print(Triangulo(6, 4).area())

# Figura se puede instanciar: NotImplementedError avisa recién al
# llamar area(). Bloquear la instanciación es tema del capítulo 13.
try:
    Figura().area()
except NotImplementedError as error:
    print(f"Error esperado: {error}")
