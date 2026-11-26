# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Concesionaria con ABM completo de autos. Auto tiene
# patente, marca, modelo y precio. Agregá agregar_auto(),
# buscar_por_patente(), listar_autos(), actualizar_precio() y
# eliminar_auto(). Usá excepciones propias para patente duplicada y auto
# no encontrado, y reutilizá buscar_por_patente() dentro de los otros
# métodos en lugar de repetir la comprobación.
# -------------------------------------------------------------------------

class PatenteDuplicadaError(Exception):
    """Indica que una patente ya está registrada."""

    pass


class AutoNoEncontrado(Exception):
    """Indica que no existe el auto solicitado."""

    pass


class Auto:
    """Auto identificado por su patente."""

    def __init__(self, patente, marca, modelo, precio):
        self._patente = patente
        self._marca = marca
        self._modelo = modelo
        self._precio = precio

    def cambiar_precio(self, nuevo_precio):
        """Actualiza el precio de venta del auto."""
        if nuevo_precio <= 0:
            raise ValueError("El precio debe ser positivo")

        self._precio = nuevo_precio

    def __str__(self):
        return (
            f"[{self._patente}] {self._marca} "
            f"{self._modelo} - ${self._precio}"
        )


class Concesionaria:
    """Gestiona un ABM de autos indexados por patente."""

    def __init__(self):
        self._autos = {}

    def agregar_auto(self, patente, marca, modelo, precio):
        """Da de alta un auto nuevo y lo devuelve."""
        if patente in self._autos:
            raise PatenteDuplicadaError(
                f"La patente {patente} ya existe"
            )

        auto = Auto(patente, marca, modelo, precio)
        self._autos[patente] = auto

        return auto

    def buscar_por_patente(self, patente):
        """Devuelve el auto con esa patente o lanza excepción."""
        auto = self._autos.get(patente)

        if auto is None:
            raise AutoNoEncontrado(
                f"No hay auto con patente {patente}"
            )

        return auto

    def listar_autos(self):
        """Devuelve la lista de autos en venta."""
        return list(self._autos.values())

    def actualizar_precio(self, patente, nuevo_precio):
        """Cambia el precio del auto indicado."""
        auto = self.buscar_por_patente(patente)
        auto.cambiar_precio(nuevo_precio)

    def eliminar_auto(self, patente):
        """Da de baja física el auto indicado."""
        self.buscar_por_patente(patente)
        del self._autos[patente]


if __name__ == "__main__":
    concesionaria = Concesionaria()
    concesionaria.agregar_auto(
        "AA123BB", "Ford", "Focus", 15000000
    )
    concesionaria.agregar_auto(
        "AC456CD", "Toyota", "Corolla", 20000000
    )

    concesionaria.actualizar_precio("AA123BB", 16000000)
    concesionaria.eliminar_auto("AC456CD")

    for auto in concesionaria.listar_autos():
        print(auto)

    try:
        concesionaria.buscar_por_patente("AC456CD")
    except AutoNoEncontrado as error:
        print(f"Error: {error}")
