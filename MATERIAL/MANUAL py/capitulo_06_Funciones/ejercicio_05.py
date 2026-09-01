# -*- coding: utf-8 -*-
# ----------------------------------------------------------------------------
# Escribí una función estadisticas(numeros) que reciba una lista y devuelva
# la suma, el promedio, el mínimo y el máximo.
# Después llamala y desempaquetá los cuatro valores.
#
# NOTA: En la línea 19 observamos una asignación múltiple, que permite asignar
# varios valores a la vez. En este caso, la función estadisticas devuelve una
# tupla con cuatro valores, y los estamos desempaquetando en cuatro variables
# distintas.
# ----------------------------------------------------------------------------


def estadisticas(numeros):
    suma = sum(numeros)
    promedio = suma / len(numeros)
    minimo = min(numeros)
    maximo = max(numeros)
    return suma, promedio, minimo, maximo


s, p, mi, ma = estadisticas([7, 3, 9, 5, 8, 2, 10])

print(f"Suma: {s}, Promedio: {p:.2f}, Mín: {mi}, Máx: {ma}")
