# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Torneo que contenga equipos por composición y un
# método agregar_equipo() que rechace la operación si ya se llegó al
# máximo. Definí el máximo como una constante del módulo, en MAYÚSCULAS,
# en vez de escribir el número suelto en el código. Usá una excepción
# propia TorneoLlenoError y sumá listar_equipos().
# -------------------------------------------------------------------------

MAX_EQUIPOS = 8


class TorneoLlenoError(Exception):
    """Indica que el torneo alcanzó el máximo de equipos."""

    pass


class Equipo:
    """Equipo participante de un torneo."""

    def __init__(self, nombre):
        self._nombre = nombre

    def __str__(self):
        return self._nombre


class Torneo:
    """Torneo con un cupo máximo de equipos."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._equipos = []

    def cupo_disponible(self):
        """Cuántos equipos más entran en el torneo."""
        return MAX_EQUIPOS - len(self._equipos)

    def agregar_equipo(self, equipo):
        """Inscribe un equipo si queda cupo."""
        if self.cupo_disponible() <= 0:
            raise TorneoLlenoError(
                f"El torneo ya tiene {MAX_EQUIPOS} equipos"
            )

        self._equipos.append(equipo)

    def listar_equipos(self):
        """Imprime los equipos inscriptos."""
        print(f"{self._nombre}:")

        for equipo in self._equipos:
            print(f"  {equipo}")


if __name__ == "__main__":
    torneo = Torneo("Copa Argentina")

    for numero in range(MAX_EQUIPOS):
        torneo.agregar_equipo(Equipo(f"Equipo {numero + 1}"))

    torneo.listar_equipos()
    print(f"Cupo disponible: {torneo.cupo_disponible()}")

    try:
        torneo.agregar_equipo(Equipo("Equipo 9"))
    except TorneoLlenoError as error:
        print(f"Error: {error}")
