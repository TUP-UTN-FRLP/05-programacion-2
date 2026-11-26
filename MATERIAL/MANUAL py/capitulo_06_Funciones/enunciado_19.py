# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# Enunciado 19:
# Escribí una función resumen(numeros) que reciba una lista
# de números y devuelva un diccionario con las claves:
# "suma", "promedio", "min", "max" y "cantidad".
# -----------------------------------------------------------


def resumen(numeros):
    return {
        "suma": sum(numeros),
        "promedio": sum(numeros) / len(numeros),
        "min": min(numeros),
        "max": max(numeros),
        "cantidad": len(numeros)
    }


r = resumen([7, 3, 9, 5, 8, 2, 10])

print(r)
print(f"Promedio: {r['promedio']:.2f}")
