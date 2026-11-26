# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Compará namedtuple con dataclass. Definí PuntoTupla con namedtuple y
# PuntoClase con @dataclass, ambos con x e y. Comprobá que los dos
# comparan por valor y se imprimen legibles, y mostrá dos diferencias:
# la namedtuple se puede desempaquetar e indexar como una tupla, y la
# dataclass admite métodos propios y valores por defecto.
# -------------------------------------------------------------------------

import math
from collections import namedtuple
from dataclasses import dataclass

PuntoTupla = namedtuple("PuntoTupla", ["x", "y"])


@dataclass
class PuntoClase:
    """Punto del plano que además sabe calcular distancias."""

    x: float = 0.0
    y: float = 0.0

    def distancia_al_origen(self):
        """Distancia euclidiana desde (0, 0)."""
        return math.hypot(self.x, self.y)


if __name__ == "__main__":
    tupla = PuntoTupla(3, 4)
    clase = PuntoClase(3, 4)

    print(tupla)
    print(clase)

    # Las dos comparan por valor, sin escribir __eq__.
    print(tupla == PuntoTupla(3, 4))
    print(clase == PuntoClase(3, 4))

    # Solo la namedtuple es una tupla: se indexa y se desempaqueta.
    print(tupla[0], tupla[1])
    x, y = tupla
    print(x, y)

    # Solo la dataclass tiene métodos propios y defaults.
    print(f"{clase.distancia_al_origen():.2f}")
    print(PuntoClase())

    # Hoy se prefiere dataclass; namedtuple sigue vivo en código
    # heredado y donde hace falta que el objeto sea una tupla.
