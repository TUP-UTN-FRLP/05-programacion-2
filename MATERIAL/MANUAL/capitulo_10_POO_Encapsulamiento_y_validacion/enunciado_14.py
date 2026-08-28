# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Circulo con _radio privado (positivo). Properties de
# solo lectura: area, perimetro, diametro. Un setter para radio que
# valide.
# -------------------------------------------------------------------------

import math


class Circulo:
    def __init__(self, radio):
        self.radio = radio

    @property
    def radio(self):
        return self._radio

    @radio.setter
    def radio(self, valor):
        if valor <= 0:
            raise ValueError("El radio debe ser positivo")

        self._radio = valor

    @property
    def area(self):
        return math.pi * self._radio ** 2

    @property
    def perimetro(self):
        return 2 * math.pi * self._radio

    @property
    def diametro(self):
        return 2 * self._radio


c = Circulo(5)

print(c.area, c.perimetro, c.diametro)
