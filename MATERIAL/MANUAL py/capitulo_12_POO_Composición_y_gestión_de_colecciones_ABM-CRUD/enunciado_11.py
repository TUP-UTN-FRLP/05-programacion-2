# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Baja lógica: hacé una clase Club con ABM de Socio, con numero y
# nombre. Dar de baja no debe borrar al socio, sino marcarlo como
# inactivo, para no perder el historial. Sumale listar_activos(),
# listar_todos() y reactivar(numero). El alta debe rechazar números
# repetidos y la baja debe fallar si el socio no existe.
# -------------------------------------------------------------------------

class SocioNoEncontrado(Exception):
    """Indica que no existe el socio solicitado."""

    pass


class NumeroDuplicadoError(Exception):
    """Indica que el número de socio ya está usado."""

    pass


class Socio:
    """Socio del club con estado de alta lógico."""

    def __init__(self, numero, nombre):
        self._numero = numero
        self._nombre = nombre
        self._activo = True

    def esta_activo(self):
        """Informa si el socio está activo."""
        return self._activo

    def dar_de_baja(self):
        """Marca al socio como inactivo sin borrarlo."""
        self._activo = False

    def reactivar(self):
        """Vuelve a marcar al socio como activo."""
        self._activo = True

    def __str__(self):
        estado = "activo" if self._activo else "de baja"
        return f"[{self._numero}] {self._nombre} ({estado})"


class Club:
    """Club que aplica baja lógica sobre sus socios."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._socios = {}

    def asociar(self, numero, nombre):
        """Da de alta un socio nuevo y lo devuelve."""
        if numero in self._socios:
            raise NumeroDuplicadoError(
                f"El socio {numero} ya existe"
            )

        socio = Socio(numero, nombre)
        self._socios[numero] = socio

        return socio

    def buscar(self, numero):
        """Devuelve el socio pedido o lanza excepción."""
        socio = self._socios.get(numero)

        if socio is None:
            raise SocioNoEncontrado(
                f"No existe el socio {numero}"
            )

        return socio

    def dar_de_baja(self, numero):
        """Marca al socio como inactivo (baja lógica)."""
        self.buscar(numero).dar_de_baja()

    def reactivar(self, numero):
        """Vuelve a poner activo a un socio dado de baja."""
        self.buscar(numero).reactivar()

    def listar_activos(self):
        """Devuelve solo los socios activos."""
        return [
            socio
            for socio in self._socios.values()
            if socio.esta_activo()
        ]

    def listar_todos(self):
        """Devuelve todos los socios, activos o no."""
        return list(self._socios.values())


if __name__ == "__main__":
    club = Club("Club Estudiantes")
    club.asociar(1, "Ana")
    club.asociar(2, "Juan")
    club.asociar(3, "Pedro")

    club.dar_de_baja(2)

    print("Activos:")
    for socio in club.listar_activos():
        print(f"  {socio}")

    print("Todos (el historial se conserva):")
    for socio in club.listar_todos():
        print(f"  {socio}")

    club.reactivar(2)
    print(club.buscar(2))
