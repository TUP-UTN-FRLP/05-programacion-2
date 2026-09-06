# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Vuelo con origen, destino y sus pasajeros. Cada
# Pasajero tiene nombre, dni y asiento. Como el asiento identifica de
# forma única al pasajero dentro del vuelo, guardá los pasajeros en un
# diccionario {asiento: Pasajero} en lugar de una lista: la búsqueda
# deja de recorrer todo. Agregá asignar_pasajero(), que rechace un
# asiento ya tomado, buscar_por_asiento() y listar_pasajeros().
# -------------------------------------------------------------------------

class AsientoOcupadoError(Exception):
    """Indica que un asiento ya fue asignado."""

    pass


class AsientoLibre(Exception):
    """Indica que no hay pasajero en ese asiento."""

    pass


class Pasajero:
    """Pasajero con nombre, DNI y asiento asignado."""

    def __init__(self, nombre, dni, asiento):
        self._nombre = nombre
        self._dni = dni
        self._asiento = asiento

    def asiento(self):
        """Devuelve el asiento asignado."""
        return self._asiento

    def __str__(self):
        return f"{self._asiento}: {self._nombre} ({self._dni})"


class Vuelo:
    """Vuelo que administra sus pasajeros por asiento."""

    def __init__(self, origen, destino):
        self._origen = origen
        self._destino = destino
        self._pasajeros = {}

    def asignar_pasajero(self, pasajero):
        """Sienta al pasajero si su asiento está libre."""
        asiento = pasajero.asiento()

        if asiento in self._pasajeros:
            raise AsientoOcupadoError(
                f"El asiento {asiento} ya está ocupado"
            )

        self._pasajeros[asiento] = pasajero

    def buscar_por_asiento(self, asiento):
        """Devuelve el pasajero de ese asiento o lanza excepción."""
        pasajero = self._pasajeros.get(asiento)

        if pasajero is None:
            raise AsientoLibre(
                f"El asiento {asiento} está libre"
            )

        return pasajero

    def listar_pasajeros(self):
        """Imprime el vuelo y sus pasajeros."""
        print(f"Vuelo {self._origen} - {self._destino}")

        for asiento in sorted(self._pasajeros):
            print(f"  {self._pasajeros[asiento]}")


if __name__ == "__main__":
    vuelo = Vuelo("EZE", "MAD")
    vuelo.asignar_pasajero(Pasajero("Ana", "12345678", "12A"))
    vuelo.asignar_pasajero(Pasajero("Juan", "87654321", "12B"))

    vuelo.listar_pasajeros()
    print(vuelo.buscar_por_asiento("12A"))

    try:
        vuelo.asignar_pasajero(
            Pasajero("Pedro", "11223344", "12A")
        )
    except AsientoOcupadoError as error:
        print(f"Error: {error}")
