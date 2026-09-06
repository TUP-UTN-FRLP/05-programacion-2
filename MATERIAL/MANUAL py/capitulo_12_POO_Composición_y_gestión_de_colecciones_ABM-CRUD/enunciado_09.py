# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Restaurant con un diccionario de Mesa. Cada Mesa tiene
# numero, capacidad y un estado de ocupación. Agregá abrir_mesa(),
# ocupar(numero), liberar(numero) y mesas_libres(). Importante: el
# Restaurant no debe cambiar el estado de la mesa desde afuera, tiene
# que pedírselo a la Mesa con ocupar() y liberar(). Validá que la mesa
# exista y que no se ocupe una mesa ya ocupada.
# -------------------------------------------------------------------------

class MesaNoEncontrada(Exception):
    """Indica que no existe la mesa solicitada."""

    pass


class MesaOcupadaError(Exception):
    """Indica que la mesa ya está ocupada."""

    pass


class Mesa:
    """Mesa que administra su propio estado de ocupación."""

    def __init__(self, numero, capacidad):
        self._numero = numero
        self._capacidad = capacidad
        self._ocupada = False

    def esta_ocupada(self):
        """Informa si la mesa está ocupada."""
        return self._ocupada

    def ocupar(self):
        """Marca la mesa como ocupada."""
        if self._ocupada:
            raise MesaOcupadaError(
                f"La mesa {self._numero} ya está ocupada"
            )

        self._ocupada = True

    def liberar(self):
        """Marca la mesa como libre."""
        self._ocupada = False

    def __str__(self):
        estado = "ocupada" if self._ocupada else "libre"
        return (
            f"Mesa {self._numero} "
            f"(cap. {self._capacidad}) - {estado}"
        )


class Restaurant:
    """Restaurant que gestiona sus mesas por número."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._mesas = {}

    def abrir_mesa(self, numero, capacidad):
        """Suma una mesa nueva al salón."""
        self._mesas[numero] = Mesa(numero, capacidad)

    def buscar_mesa(self, numero):
        """Devuelve la mesa pedida o lanza excepción."""
        mesa = self._mesas.get(numero)

        if mesa is None:
            raise MesaNoEncontrada(
                f"No existe la mesa {numero}"
            )

        return mesa

    def ocupar(self, numero):
        """Le pide a la mesa que se marque como ocupada."""
        self.buscar_mesa(numero).ocupar()

    def liberar(self, numero):
        """Le pide a la mesa que se marque como libre."""
        self.buscar_mesa(numero).liberar()

    def mesas_libres(self):
        """Devuelve las mesas que no están ocupadas."""
        return [
            mesa
            for mesa in self._mesas.values()
            if not mesa.esta_ocupada()
        ]


if __name__ == "__main__":
    restaurant = Restaurant("La Trattoria")

    for numero, capacidad in [(1, 4), (2, 2), (3, 6)]:
        restaurant.abrir_mesa(numero, capacidad)

    restaurant.ocupar(2)

    for mesa in restaurant.mesas_libres():
        print(mesa)

    try:
        restaurant.ocupar(2)
    except MesaOcupadaError as error:
        print(f"Error: {error}")

    try:
        restaurant.ocupar(99)
    except MesaNoEncontrada as error:
        print(f"Error: {error}")
