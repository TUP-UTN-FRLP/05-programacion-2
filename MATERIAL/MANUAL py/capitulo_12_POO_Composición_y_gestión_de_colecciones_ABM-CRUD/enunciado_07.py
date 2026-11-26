# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Equipo con nombre y una lista de Jugador. Cada Jugador
# tiene nombre, posicion y numero. Agregá agregar_jugador(),
# jugador_por_numero(numero), que lance una excepción propia si no está,
# y alineacion(), que imprima todos los jugadores ordenados por número.
# -------------------------------------------------------------------------

class JugadorNoEncontrado(Exception):
    """Indica que no existe un jugador con el número pedido."""

    pass


class Jugador:
    """Jugador con nombre, posición y número de camiseta."""

    def __init__(self, nombre, posicion, numero):
        self._nombre = nombre
        self._posicion = posicion
        self._numero = numero

    def numero(self):
        """Devuelve el número de camiseta."""
        return self._numero

    def __str__(self):
        return (
            f"#{self._numero} {self._nombre} "
            f"({self._posicion})"
        )


class Equipo:
    """Equipo que administra una colección de jugadores."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._jugadores = []

    def agregar_jugador(self, jugador):
        """Suma un jugador al plantel."""
        self._jugadores.append(jugador)

    def jugador_por_numero(self, numero):
        """Devuelve el jugador con ese número o lanza excepción."""
        for jugador in self._jugadores:
            if jugador.numero() == numero:
                return jugador

        raise JugadorNoEncontrado(
            f"No hay jugador con número {numero}"
        )

    def alineacion(self):
        """Imprime el plantel ordenado por número de camiseta."""
        ordenados = sorted(
            self._jugadores,
            key=lambda jugador: jugador.numero(),
        )

        print(f"{self._nombre}:")

        for jugador in ordenados:
            print(f"  {jugador}")


if __name__ == "__main__":
    equipo = Equipo("Estudiantes")
    equipo.agregar_jugador(Jugador("Verón", "Volante", 11))
    equipo.agregar_jugador(Jugador("Palermo", "Delantero", 9))
    equipo.agregar_jugador(Jugador("Andújar", "Arquero", 1))

    equipo.alineacion()
    print(equipo.jugador_por_numero(9))

    try:
        equipo.jugador_por_numero(99)
    except JugadorNoEncontrado as error:
        print(f"Error: {error}")
