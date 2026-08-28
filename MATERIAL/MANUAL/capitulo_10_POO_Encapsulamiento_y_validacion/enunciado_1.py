# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Convertí la clase Punto del capítulo anterior para que x e y sean
# privados y expuestos como properties de solo lectura. El único modo de
# "cambiarlos" es crear un nuevo Punto.
# -------------------------------------------------------------------------


class Punto:
    def __init__(self, x, y):
        if not isinstance(x, (int, float)):
            raise TypeError("x debe ser numérico")

        if not isinstance(y, (int, float)):
            raise TypeError("y debe ser numérico")

        self._x = x
        self._y = y

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    def __str__(self):
        return f"({self._x}, {self._y})"


p = Punto(3, 5)

print(p.x, p.y)  # 3 5

p.x = 10  # AttributeError: property 'x' of 'Punto' object has no setter
