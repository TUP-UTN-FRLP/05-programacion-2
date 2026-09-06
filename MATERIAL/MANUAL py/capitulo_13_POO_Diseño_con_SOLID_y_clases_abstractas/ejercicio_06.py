# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Convertí Instrumento, con los métodos tocar() y afinar(), en una clase
# abstracta usando ABC y @abstractmethod. Después hacé Guitarra y Piano
# como hijas concretas. Verificá que no podés instanciar Instrumento
# directamente ni una hija que se olvide de implementar algún método.
# -------------------------------------------------------------------------

from abc import ABC, abstractmethod


class Instrumento(ABC):
    """Instrumento abstracto: todo instrumento toca y se afina."""

    def __init__(self, nombre):
        self._nombre = nombre

    @abstractmethod
    def tocar(self):
        """Produce el sonido característico del instrumento."""

    @abstractmethod
    def afinar(self):
        """Ajusta la afinación del instrumento."""


class Guitarra(Instrumento):
    """Instrumento de cuerda."""

    def tocar(self):
        print(f"Rasguido con {self._nombre}")

    def afinar(self):
        print(f"Afinando las cuerdas de {self._nombre}")


class Piano(Instrumento):
    """Instrumento de percusión con teclado."""

    def tocar(self):
        print(f"Acordes en {self._nombre}")

    def afinar(self):
        print(f"Afinando los martillos de {self._nombre}")


class Bateria(Instrumento):
    """Hija incompleta: se olvidó de implementar afinar()."""

    def tocar(self):
        print(f"Redoble en {self._nombre}")


if __name__ == "__main__":
    for instrumento in [Guitarra("Fender"), Piano("Yamaha")]:
        instrumento.tocar()
        instrumento.afinar()

    try:
        Instrumento("cualquiera")
    except TypeError as error:
        print(f"Instrumento es abstracta: {error}")

    try:
        Bateria("Ludwig")
    except TypeError as error:
        print(f"Bateria quedó incompleta: {error}")
