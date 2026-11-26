# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 01
# Definí una clase Punto con atributos x e y. Agregale un método
# mostrar() que imprima "({x}, {y})". Creá tres puntos y mostralos.
# -------------------------------------------------------------------------


class Punto:

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def mostrar(self):
        print(f"({self.x}, {self.y})")


p1 = Punto(3, 5)
p2 = Punto(-1, 4)
p3 = Punto(0, 0)


p1.mostrar()
p2.mostrar()
p3.mostrar()
