# -*- coding: utf-8 -*-
# --------------------------------------------------------
# Enunciado 2:
# Escribí una función max_de_tres(a, b, c) que devuelva
# el mayor de tres números. No uses max(), hacelo con if.
# --------------------------------------------------------


def max_de_tres(a, b, c):
    if a >= b and a >= c:
        return a

    if b >= c:
        return b

    return c


print(max_de_tres(3, 8, 5))
print(max_de_tres(10, 2, 7))
