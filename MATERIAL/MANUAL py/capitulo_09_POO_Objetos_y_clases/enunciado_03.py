# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 03
# Definí una clase Rectangulo con atributos base y altura. Agregale
# métodos area() y perimetro().
# -------------------------------------------------------------------------


class Rectangulo:

    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    def area(self):
        return self.base * self.altura

    def perimetro(self):
        return 2 * (self.base + self.altura)


r = Rectangulo(5, 3)

print(f"Área: {r.area()} unidades cuadradas")
print(f"Perímetro: {r.perimetro()} unidades")
