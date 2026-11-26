# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Enemigo con nombre, vida y un método atacar() que
# devuelve 10 de daño. Hacé Dragon(Enemigo), que ataca por 50, y
# Goblin(Enemigo), que ataca por 5. Simulá un turno recorriendo una
# lista mixta: cada enemigo ataca, se informa su estado y se acumula el
# daño total del grupo.
# -------------------------------------------------------------------------

class Enemigo:
    """Enemigo base con nombre, vida y ataque genérico."""

    def __init__(self, nombre, vida):
        self._nombre = nombre
        self._vida = vida

    def atacar(self):
        """Daño que provoca el enemigo en un turno."""
        return 10

    def __str__(self):
        return f"{self._nombre} (vida: {self._vida})"


class Dragon(Enemigo):
    """Enemigo que causa 50 puntos de daño."""

    def atacar(self):
        return 50


class Goblin(Enemigo):
    """Enemigo que causa 5 puntos de daño."""

    def atacar(self):
        return 5


enemigos = [
    Dragon("Smaug", 300),
    Goblin("Verdo", 30),
    Goblin("Rojo", 30),
    Enemigo("Sombra", 50),
]

danio_total = 0
for enemigo in enemigos:
    danio = enemigo.atacar()
    danio_total += danio
    print(f"{enemigo} ataca por {danio}")

print(f"Daño total del turno: {danio_total}")
