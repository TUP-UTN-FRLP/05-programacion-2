# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# Enunciado 8:
# Escribí una función minmax(numeros) que devuelva la tupla
# (mínimo, máximo) de una lista.
# -----------------------------------------------------------


def minmax(numeros):
    return min(numeros), max(numeros)


mi, ma = minmax([7, 3, 9, 1, 8])

print(f"Mín: {mi}, Máx: {ma}")
