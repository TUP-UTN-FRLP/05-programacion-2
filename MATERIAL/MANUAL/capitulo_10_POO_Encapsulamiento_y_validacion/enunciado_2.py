# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Ampliá la clase Rectangulo para que base y altura sean properties con
# setters que rechacen valores no positivos.
# -------------------------------------------------------------------------


class Rectangulo:
    def __init__(self, base, altura):
        self.base = base
        self.altura = altura

    @property
    def base(self):
        return self._base

    @base.setter
    def base(self, valor):
        if valor <= 0:
            raise ValueError("La base debe ser positiva")

        self._base = valor

    @property
    def altura(self):
        return self._altura

    @altura.setter
    def altura(self, valor):
        if valor <= 0:
            raise ValueError("La altura debe ser positiva")

        self._altura = valor

    @property
    def area(self):
        return self._base * self._altura


r = Rectangulo(5, 3)

print(r.area)  # 15

r.base = 10

print(r.area)  # 30

r.altura = -1  # ValueError
