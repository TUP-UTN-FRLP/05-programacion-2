# -*- coding: utf-8 -*-
# --------------------------------------------------------------
# Enunciado 6:
# Escribí una función promedio(lista) que devuelva el promedio
# de una lista de números.
# Si la lista está vacía, que devuelva 0.
# --------------------------------------------------------------


def promedio(lista):
    if len(lista) == 0:
        return 0

    return sum(lista) / len(lista)


print(promedio([7, 8, 9]))
print(promedio([]))
