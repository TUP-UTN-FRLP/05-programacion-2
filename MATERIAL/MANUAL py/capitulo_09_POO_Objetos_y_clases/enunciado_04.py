# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 04
# Definí una clase Circulo con atributo radio. Agregale métodos area()
# y perimetro(). Usá math.pi.
# -------------------------------------------------------------------------

import math


class Circulo:

    def __init__(self, radio):
        self.radio = radio

    def area(self):
        return math.pi * self.radio ** 2

    def perimetro(self):
        return 2 * math.pi * self.radio


c = Circulo(5)

print(f"Área: {c.area():.2f} unidades cuadradas")
print(f"Perímetro: {c.perimetro():.2f} unidades")
