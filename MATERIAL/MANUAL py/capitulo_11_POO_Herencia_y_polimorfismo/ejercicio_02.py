# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Partí de la clase Animal con respirar(). Hacé que Perro agregue un
# método ladrar() que imprima "¡Guau!". Creá un perro, hacelo respirar
# y ladrar. Después creá un Animal genérico y comprobá que no puede
# ladrar: el método existe solo en la hija.
# -------------------------------------------------------------------------

class Animal:
    """Animal base con la capacidad de respirar."""

    def respirar(self):
        """Imprime que el animal está respirando."""
        print("Respirando...")


class Perro(Animal):
    """Animal que agrega el comportamiento de ladrar."""

    def ladrar(self):
        """Imprime el ladrido del perro."""
        print("¡Guau!")


firulais = Perro()
firulais.respirar()
firulais.ladrar()

generico = Animal()
generico.respirar()

try:
    generico.ladrar()
except AttributeError as error:
    print(f"Error esperado: {error}")
