# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Definí una clase Animal con un método respirar() que imprima
# "Respirando...". Después definí Perro(Animal) sin agregar nada. Creá
# un perro y hacelo respirar. Comprobá con isinstance que es al mismo
# tiempo Perro y Animal.
# -------------------------------------------------------------------------

class Animal:
    """Animal base con la capacidad de respirar."""

    def respirar(self):
        """Imprime que el animal está respirando."""
        print("Respirando...")


class Perro(Animal):
    """Perro que hereda todo sin agregar comportamiento propio."""

    pass


pichicho = Perro()
pichicho.respirar()

print(isinstance(pichicho, Perro))
print(isinstance(pichicho, Animal))
print(isinstance(pichicho, object))
