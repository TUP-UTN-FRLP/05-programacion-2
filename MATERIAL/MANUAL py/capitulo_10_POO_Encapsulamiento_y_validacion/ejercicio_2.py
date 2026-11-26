# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Circulo con un atributo _radio privado. Exponé radio como
# property con setter que rechace valores negativos o cero, lanzando
# ValueError.
#
# Además, exponé area como property de solo lectura que devuelva pi * radio
# ** 2.
#
# Conservar el uso de math y las pruebas del ejercicio.
# -------------------------------------------------------------------------


import math


class Circulo:
    def __init__(self, radio):
        self.radio = radio          # pasa por el setter (valida)

    @property
    def radio(self):
        return self._radio

    @radio.setter
    def radio(self, valor):
        if valor <= 0:
            raise ValueError("El radio debe ser mayor que cero")
        self._radio = valor

    @property
    def area(self):
        return math.pi * self._radio ** 2


c = Circulo(5)
print(c.radio)                      # 5
print(c.area)                       # 78.53981633974483

c.radio = 10
print(c.area)                       # 314.1592653589793

# El setter rechaza cero y negativos.
try:
    c.radio = -3
except ValueError as e:
    print("Error:", e)

try:
    Circulo(0)
except ValueError as e:
    print("Error:", e)

# area es de solo lectura: no tiene setter.
try:
    c.area = 100
except AttributeError as e:
    print("Error:", e)
