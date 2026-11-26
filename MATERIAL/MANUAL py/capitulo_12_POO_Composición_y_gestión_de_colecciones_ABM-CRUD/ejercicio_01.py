# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Modelá una Casa que tiene un objeto Direccion como atributo, con
# calle, número y ciudad. Después imprimí la casa incluyendo la
# dirección completa. No uses herencia: una Casa no es una dirección,
# tiene una.
# -------------------------------------------------------------------------

class Direccion:
    """Dirección postal, pensada para vivir dentro de otras clases."""

    def __init__(self, calle, numero, ciudad):
        self._calle = calle
        self._numero = numero
        self._ciudad = ciudad

    def __str__(self):
        return f"{self._calle} {self._numero}, {self._ciudad}"


class Casa:
    """Casa compuesta por un objeto Direccion."""

    def __init__(self, dueno, direccion):
        self._dueno = dueno
        self._direccion = direccion

    def __str__(self):
        return f"Casa de {self._dueno} en {self._direccion}"


if __name__ == "__main__":
    direccion = Direccion("Av. 7", 1234, "La Plata")
    casa = Casa("Ana Perez", direccion)

    print(casa)
