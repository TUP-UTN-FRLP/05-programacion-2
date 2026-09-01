# -*- coding: utf-8 -*-
# ----------------------------------------------------
# Enunciado 18:
# Escribí una función top_n(lista, n=3) que devuelva
# los n valores más grandes de una lista.
# Por defecto, n debe ser 3.
# ----------------------------------------------------


def top_n(lista, n=3):
    return sorted(lista, reverse=True)[:n]


notas = [4, 8, 3, 9, 6, 10, 2, 7]

print(top_n(notas))
print(top_n(notas, 5))
