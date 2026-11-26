# -*- coding: utf-8 -*-
# ---------------------------------------------------
# Enunciado 4:
# Escribí una función factorial(n) que devuelva n!.
# Por ejemplo: factorial(5) = 120.
# ---------------------------------------------------


def factorial(n):
    resultado = 1

    for i in range(1, n + 1):
        resultado *= i

    return resultado


print(factorial(5))
print(factorial(10))
print(factorial(0))
