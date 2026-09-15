# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Instrumento con atributo nombre y método tocar() que
# devuelve "...". Hacé Guitarra(Instrumento), Piano(Instrumento) y
# Bateria(Instrumento) que sobrescriban tocar() con mensajes distintos.
# Después creá una lista mixta y hacé que cada uno toque.
# -------------------------------------------------------------------------

class Instrumento:
    """Instrumento con nombre y sonido genérico."""

    def __init__(self, nombre):
        self._nombre = nombre

    def tocar(self):
        """Sonido por defecto de un instrumento sin especializar."""
        return "..."

    def __str__(self):
        return f"{self._nombre}: {self.tocar()}"


class Guitarra(Instrumento):
    """Guitarra con su propia forma de sonar."""

    def tocar(self):
        return "Rasguido de guitarra"


class Piano(Instrumento):
    """Piano con su propia forma de sonar."""

    def tocar(self):
        return "Acorde de piano"


class Bateria(Instrumento):
    """Batería con su propia forma de sonar."""

    def tocar(self):
        return "Redoble de batería"


banda = [
    Guitarra("Fender"),
    Piano("Yamaha"),
    Bateria("Ludwig"),
]

for instrumento in banda:
    print(instrumento.tocar())
