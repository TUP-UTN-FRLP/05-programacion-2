# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Combinando ABC y dataclass: hacé una jerarquía Item (ABC) que declare
# precio_final() como abstracto, e ItemNormal e ItemConDescuento como
# dataclasses que lo implementen. Comprobá que las dos herramientas se
# combinan sin problemas y que Item sigue sin poder instanciarse.
# -------------------------------------------------------------------------

from abc import ABC, abstractmethod
from dataclasses import dataclass


class Item(ABC):
    """Item abstracto: sabe decir cuánto se cobra por él."""

    @abstractmethod
    def precio_final(self) -> float:
        """Importe a cobrar por una unidad del item."""


@dataclass
class ItemNormal(Item):
    """Item cuyo precio final es el de lista."""

    nombre: str
    precio: float

    def precio_final(self) -> float:
        return self.precio


@dataclass
class ItemConDescuento(Item):
    """Item con un descuento porcentual aplicado."""

    nombre: str
    precio: float
    descuento: float

    def precio_final(self) -> float:
        return self.precio * (1 - self.descuento / 100)


def total(items: list[Item]) -> float:
    """Suma los precios finales sin distinguir tipos."""
    return sum(item.precio_final() for item in items)


if __name__ == "__main__":
    items: list[Item] = [
        ItemNormal("Yerba", 3500),
        ItemConDescuento("Bebida", 1000, 15),
    ]

    for item in items:
        print(f"  {item} -> ${item.precio_final():.2f}")

    print(f"Total: ${total(items):.2f}")

    try:
        Item()
    except TypeError as error:
        print(f"Item es abstracta: {error}")
