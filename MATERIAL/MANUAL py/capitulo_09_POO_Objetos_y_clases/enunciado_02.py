# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 02
# Sumale a Punto un método distancia_al_origen() que devuelva la
# distancia del punto al origen. Usá math.sqrt.
# -------------------------------------------------------------------------

import math


class Punto:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def mostrar(self):
        print(f"({self.x}, {self.y})")

    def distancia_al_origen(self):
        return math.sqrt(self.x ** 2 + self.y ** 2)


p = Punto(3, 4)
print(p.distancia_al_origen())
