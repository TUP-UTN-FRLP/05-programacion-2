# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Extendé el ejercicio 12: sumale una clase Reserva, con habitacion,
# huesped y dias, y una lista de reservas dentro del hotel. Incorporá
# reservar(numero, huesped, dias). Distinguí los dos errores posibles
# con excepciones distintas: que la habitación no exista y que exista
# pero ya esté ocupada. No son lo mismo y el usuario necesita saber
# cuál de los dos ocurrió.
# -------------------------------------------------------------------------

class HabitacionNoEncontrada(Exception):
    """Indica que no existe la habitación solicitada."""

    pass


class HabitacionNoDisponible(Exception):
    """Indica que la habitación existe pero está ocupada."""

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

    def precio(self):
        """Devuelve el precio por noche."""
        return self._precio

    def esta_disponible(self):
        """Informa si la habitación se puede reservar."""
        return self._disponible

    def ocupar(self):
        """Marca la habitación como no disponible."""
        self._disponible = False

    def __str__(self):
        return (
            f"Hab {self._numero} ({self._tipo}) - "
            f"${self._precio}/noche"
        )


class Reserva:
    """Reserva que referencia una habitación del hotel."""

    def __init__(self, habitacion, huesped, dias):
        self._habitacion = habitacion
        self._huesped = huesped
        self._dias = dias

    def importe(self):
        """Precio por noche multiplicado por los días."""
        return self._habitacion.precio() * self._dias

    def __str__(self):
        return (
            f"{self._huesped} en hab "
            f"{self._habitacion.numero()} por {self._dias} "
            f"días: ${self.importe()}"
        )


class Hotel:
    """Hotel que gestiona habitaciones y reservas."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._habitaciones = {}
        self._reservas = []

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

    def reservar(self, numero, huesped, dias):
        """Reserva una habitación libre y devuelve la reserva."""
        habitacion = self.buscar_habitacion(numero)

        if not habitacion.esta_disponible():
            raise HabitacionNoDisponible(
                f"La habitación {numero} ya está ocupada"
            )

        reserva = Reserva(habitacion, huesped, dias)
        self._reservas.append(reserva)
        habitacion.ocupar()

        return reserva

    def listar_reservas(self):
        """Devuelve las reservas registradas."""
        return list(self._reservas)


if __name__ == "__main__":
    hotel = Hotel("Hotel Central")
    hotel.agregar_habitacion(101, "single", 15000)
    hotel.agregar_habitacion(102, "doble", 22000)

    print(hotel.reservar(101, "Ana Perez", 3))

    try:
        hotel.reservar(101, "Otro huésped", 2)
    except HabitacionNoDisponible as error:
        print(f"Ocupada: {error}")

    try:
        hotel.reservar(999, "Otro huésped", 2)
    except HabitacionNoEncontrada as error:
        print(f"Inexistente: {error}")
