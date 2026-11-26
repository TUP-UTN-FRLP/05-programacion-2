# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Creá una sola Direccion y dos Personas que la compartan. Mudá la
# dirección con mudar() y comprobá que las dos personas ven el cambio:
# guardan una referencia al mismo objeto, no una copia. Después hacé lo
# mismo con copy.deepcopy y verificá que ahí sí quedan independientes.
# -------------------------------------------------------------------------

import copy


class Direccion:
    """Dirección postal que puede cambiar de valores."""

    def __init__(self, calle, numero, ciudad):
        self._calle = calle
        self._numero = numero
        self._ciudad = ciudad

    def mudar(self, calle, numero):
        """Cambia calle y número conservando la ciudad."""
        self._calle = calle
        self._numero = numero

    def __str__(self):
        return f"{self._calle} {self._numero}, {self._ciudad}"


class Persona:
    """Persona que tiene una Direccion."""

    def __init__(self, nombre, direccion):
        self._nombre = nombre
        self._direccion = direccion

    def __str__(self):
        return f"{self._nombre}: {self._direccion}"


if __name__ == "__main__":
    familiar = Direccion("Av. 7", 1234, "La Plata")

    madre = Persona("Ana", familiar)
    hijo = Persona("Pedro", familiar)

    print("Antes de la mudanza:")
    print(f"  {madre}")
    print(f"  {hijo}")

    familiar.mudar("Calle 50", 900)

    print("Después de la mudanza (cambiaron los dos):")
    print(f"  {madre}")
    print(f"  {hijo}")

    # Con una copia profunda, la dirección del hijo es otro objeto.
    independiente = Persona("Lucía", copy.deepcopy(familiar))
    familiar.mudar("Diagonal 74", 55)

    print("Con deepcopy, Lucía no se entera del cambio:")
    print(f"  {madre}")
    print(f"  {independiente}")
