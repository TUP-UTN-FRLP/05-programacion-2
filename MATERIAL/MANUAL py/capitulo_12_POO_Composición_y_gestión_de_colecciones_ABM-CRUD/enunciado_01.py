# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Direccion con calle, numero y ciudad. Después hacé
# Persona que tenga una Direccion como atributo, usando composición.
# Imprimí una persona con su dirección completa. Fijate que Persona no
# reimplementa el formato de la dirección: se lo delega a Direccion.
# -------------------------------------------------------------------------

class Direccion:
    """Dirección postal, pensada para vivir dentro de otras clases."""

    def __init__(self, calle, numero, ciudad):
        self._calle = calle
        self._numero = numero
        self._ciudad = ciudad

    def __str__(self):
        return f"{self._calle} {self._numero}, {self._ciudad}"


class Persona:
    """Persona que tiene una Direccion como atributo."""

    def __init__(self, nombre, direccion):
        self._nombre = nombre
        self._direccion = direccion

    def __str__(self):
        return f"{self._nombre} vive en {self._direccion}"


if __name__ == "__main__":
    direccion = Direccion("Av. 7", 1234, "La Plata")
    persona = Persona("Ana Perez", direccion)

    print(persona)
