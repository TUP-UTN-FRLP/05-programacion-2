# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Te dan este bucle, que pregunta el tipo antes de actuar:
#
#     for cliente in clientes:
#         if isinstance(cliente, ClienteVIP):
#             descuento = 20
#         elif isinstance(cliente, ClientePremium):
#             descuento = 35
#         else:
#             descuento = 0
#         print(cliente._nombre, descuento)
#
# Reescribilo con polimorfismo: cada clase debe saber su propio
# descuento(). El bucle final no debe preguntar ningún tipo, y agregar
# una categoría nueva no debe obligar a tocarlo.
# -------------------------------------------------------------------------

class Cliente:
    """Cliente sin beneficios: no tiene descuento."""

    def __init__(self, nombre):
        self._nombre = nombre

    def descuento(self):
        """Porcentaje de descuento de la categoría."""
        return 0

    def __str__(self):
        return f"{self._nombre}: {self.descuento()}% de descuento"


class ClienteVIP(Cliente):
    """Cliente con 20 por ciento de descuento."""

    def descuento(self):
        return 20


class ClientePremium(Cliente):
    """Cliente con 35 por ciento de descuento."""

    def descuento(self):
        return 35


class ClienteMayorista(Cliente):
    """Categoría agregada después: el bucle no cambió."""

    def descuento(self):
        return 40


clientes = [
    Cliente("Ana"),
    ClienteVIP("Juan"),
    ClientePremium("Pedro"),
    ClienteMayorista("Lucía"),
]

for cliente in clientes:
    print(cliente)
