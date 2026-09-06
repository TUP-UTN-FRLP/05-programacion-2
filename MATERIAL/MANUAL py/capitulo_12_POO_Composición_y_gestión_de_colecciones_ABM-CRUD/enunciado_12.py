# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Hotel con nombre y un diccionario de Habitacion. Cada
# Habitacion tiene numero, tipo, precio por noche y disponibilidad.
# Agregá agregar_habitacion(), buscar_habitacion(numero), que lance
# excepción si no existe, y habitaciones_disponibles().
# -------------------------------------------------------------------------

class HabitacionNoEncontrada(Exception):
    """Indica que no existe la habitación solicitada."""

    pass


class Habitacion:
    """Habitación con tipo, precio y disponibilidad."""

    def __init__(self, numero, tipo, precio):
        self._numero = numero
        self._tipo = tipo
        self._precio = precio
        self._disponible = True

    def numero(self):
        """Devuelve el número de habitación."""
        return self._numero

    def esta_disponible(self):
        """Informa si la habitación se puede reservar."""
        return self._disponible

    def ocupar(self):
        """Marca la habitación como no disponible."""
        self._disponible = False

    def liberar(self):
        """Marca la habitación como disponible."""
        self._disponible = True

    def __str__(self):
        return (
            f"Hab {self._numero} ({self._tipo}) - "
            f"${self._precio}/noche"
        )


class Hotel:
    """Hotel que administra habitaciones por número."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._habitaciones = {}

    def agregar_habitacion(self, numero, tipo, precio):
        """Suma una habitación al hotel."""
        self._habitaciones[numero] = Habitacion(
            numero, tipo, precio
        )

    def buscar_habitacion(self, numero):
        """Devuelve la habitación pedida o lanza excepción."""
        habitacion = self._habitaciones.get(numero)

        if habitacion is None:
            raise HabitacionNoEncontrada(
                f"No existe la habitación {numero}"
            )

        return habitacion

    def habitaciones_disponibles(self):
        """Devuelve las habitaciones libres."""
        return [
            habitacion
            for habitacion in self._habitaciones.values()
            if habitacion.esta_disponible()
        ]


if __name__ == "__main__":
    hotel = Hotel("Hotel Central")
    hotel.agregar_habitacion(101, "single", 15000)
    hotel.agregar_habitacion(102, "doble", 22000)

    for habitacion in hotel.habitaciones_disponibles():
        print(habitacion)

    try:
        hotel.buscar_habitacion(999)
    except HabitacionNoEncontrada as error:
        print(f"Error: {error}")
