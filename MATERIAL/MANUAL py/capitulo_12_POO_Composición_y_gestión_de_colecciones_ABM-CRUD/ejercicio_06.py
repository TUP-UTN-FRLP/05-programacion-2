# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Agenda con ABM completo de contactos. Cada Contacto
# tiene nombre y telefono. Agregá agregar_contacto(), buscar(),
# listar(), actualizar_telefono() y eliminar(). Usá las excepciones
# propias ContactoNoEncontrado y NombreDuplicadoError.
# -------------------------------------------------------------------------

class ContactoNoEncontrado(Exception):
    """Indica que no existe el contacto solicitado."""

    pass


class NombreDuplicadoError(Exception):
    """Indica que el nombre ya existe en la agenda."""

    pass


class Contacto:
    """Contacto con nombre y teléfono."""

    def __init__(self, nombre, telefono):
        self._nombre = nombre
        self._telefono = telefono

    def cambiar_telefono(self, nuevo_telefono):
        """Actualiza el teléfono del contacto."""
        self._telefono = nuevo_telefono

    def __str__(self):
        return f"{self._nombre}: {self._telefono}"


class Agenda:
    """Gestiona un ABM de contactos indexados por nombre."""

    def __init__(self):
        self._contactos = {}

    def agregar_contacto(self, nombre, telefono):
        """Da de alta un contacto nuevo y lo devuelve."""
        if nombre in self._contactos:
            raise NombreDuplicadoError(
                f"{nombre} ya existe en la agenda"
            )

        contacto = Contacto(nombre, telefono)
        self._contactos[nombre] = contacto

        return contacto

    def buscar(self, nombre):
        """Devuelve el contacto pedido o lanza excepción."""
        contacto = self._contactos.get(nombre)

        if contacto is None:
            raise ContactoNoEncontrado(
                f"No hay contacto llamado {nombre}"
            )

        return contacto

    def listar(self):
        """Devuelve todos los contactos de la agenda."""
        return list(self._contactos.values())

    def actualizar_telefono(self, nombre, nuevo_telefono):
        """Le pide al contacto que cambie su teléfono."""
        self.buscar(nombre).cambiar_telefono(nuevo_telefono)

    def eliminar(self, nombre):
        """Elimina el contacto indicado de la agenda."""
        self.buscar(nombre)
        del self._contactos[nombre]


if __name__ == "__main__":
    agenda = Agenda()
    agenda.agregar_contacto("Ana", "221-1234")
    agenda.agregar_contacto("Juan", "221-5678")

    agenda.actualizar_telefono("Ana", "221-9999")
    agenda.eliminar("Juan")

    for contacto in agenda.listar():
        print(contacto)

    try:
        agenda.buscar("Juan")
    except ContactoNoEncontrado as error:
        print(f"Error: {error}")
