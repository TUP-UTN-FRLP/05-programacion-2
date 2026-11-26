# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Animal con nombre y un método sonido() que devuelve
# "...". Hacé Perro(Animal), Gato(Animal) y Vaca(Animal) que
# sobrescriban sonido() con "Guau", "Miau" y "Muu". Recorré una lista
# mixta que incluya también un Animal genérico y hacé que cada uno
# hable: el genérico responde con la versión heredada del padre.
# -------------------------------------------------------------------------

class Animal:
    """Animal base con nombre y sonido genérico."""

    def __init__(self, nombre):
        self._nombre = nombre

    def sonido(self):
        """Sonido por defecto de un animal sin especializar."""
        return "..."

    def hablar(self):
        """Imprime el nombre del animal junto a su sonido."""
        print(f"{self._nombre} dice: {self.sonido()}")


class Perro(Animal):
    """Animal cuyo sonido es Guau."""

    def sonido(self):
        return "Guau"


class Gato(Animal):
    """Animal cuyo sonido es Miau."""

    def sonido(self):
        return "Miau"


class Vaca(Animal):
    """Animal cuyo sonido es Muu."""

    def sonido(self):
        return "Muu"


animales = [
    Perro("Firulais"),
    Gato("Michi"),
    Vaca("Lola"),
    Animal("Bicho"),
]

for animal in animales:
    animal.hablar()
