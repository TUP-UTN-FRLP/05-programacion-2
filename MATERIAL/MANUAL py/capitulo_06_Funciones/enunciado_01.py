# -*- coding: utf-8 -*-
# ---------------------------------------------------
# Enunciado 1:
# Escribí una función cuadrado(x) que devuelva x².
# Usala para imprimir los cuadrados del 1 al 10.
#
# NOTA: El caracter superíndice ² se puede escribir
# con la combinación de teclas Alt + 0178
# ---------------------------------------------------


def cuadrado(x):
    return x ** 2


for i in range(1, 11):
    print(f"{i}² = {cuadrado(i)}")
