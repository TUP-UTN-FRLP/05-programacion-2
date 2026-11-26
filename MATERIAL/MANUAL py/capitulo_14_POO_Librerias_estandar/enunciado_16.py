# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Simulá una cola de atención con deque. Definí ColaAtencion con
# agregar_persona(nombre), que suma al final; atender_siguiente(), que
# saca del principio; y agregar_urgente(nombre), que inserta al
# principio. Explicá en un comentario por qué deque y no list.
# -------------------------------------------------------------------------

from collections import deque


class ColaAtencion:
    """Cola de atención eficiente en los dos extremos."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._cola = deque()

    def agregar_persona(self, nombre):
        """Suma una persona al final de la cola."""
        self._cola.append(nombre)

    def agregar_urgente(self, nombre):
        """Inserta una persona al principio de la cola."""
        self._cola.appendleft(nombre)

    def atender_siguiente(self):
        """Saca y devuelve a la primera persona, o None si no hay."""
        if not self._cola:
            return None

        return self._cola.popleft()

    def __len__(self):
        return len(self._cola)

    def __str__(self):
        if not self._cola:
            return f"{self._nombre}: (vacía)"

        return f"{self._nombre}: " + " -> ".join(self._cola)


if __name__ == "__main__":
    # En una lista, insertar o sacar del principio obliga a correr
    # todos los elementos: es O(n). En un deque es O(1). Para una
    # cola, que trabaja siempre en los extremos, deque gana.
    cola = ColaAtencion("Mesa de entradas")

    for persona in ["Ana", "Juan", "Pedro"]:
        cola.agregar_persona(persona)

    print(cola)

    cola.agregar_urgente("Emergencia")
    print(cola)

    print(f"Atendiendo a: {cola.atender_siguiente()}")
    print(f"Quedan {len(cola)} personas")
