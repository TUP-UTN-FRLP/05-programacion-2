# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Forma3D con un método abstracto conceptual volumen().
# Definí Cubo(lado), Esfera(radio) y Cilindro(radio, altura). Cada una
# implementa volumen() con su fórmula. Recorré una lista mixta y mostrá
# el volumen de cada una redondeado a dos decimales.
# -------------------------------------------------------------------------

import math


class Forma3D:
    """Forma tridimensional cuyo volumen implementan sus hijas."""

    def volumen(self):
        """Contrato que toda forma concreta debe cumplir."""
        raise NotImplementedError(
            f"La clase {type(self).__name__} debe implementar volumen()"
        )

    def __str__(self):
        return f"{type(self).__name__}: {self.volumen():.2f}"


class Cubo(Forma3D):
    """Cubo definido por la longitud de su lado."""

    def __init__(self, lado):
        self._lado = lado

    def volumen(self):
        return self._lado ** 3


class Esfera(Forma3D):
    """Esfera definida por su radio."""

    def __init__(self, radio):
        self._radio = radio

    def volumen(self):
        return 4 / 3 * math.pi * self._radio ** 3


class Cilindro(Forma3D):
    """Cilindro definido por radio y altura."""

    def __init__(self, radio, altura):
        self._radio = radio
        self._altura = altura

    def volumen(self):
        return math.pi * self._radio ** 2 * self._altura


formas = [
    Cubo(3),
    Esfera(2),
    Cilindro(2, 5),
]

for forma in formas:
    print(forma)
