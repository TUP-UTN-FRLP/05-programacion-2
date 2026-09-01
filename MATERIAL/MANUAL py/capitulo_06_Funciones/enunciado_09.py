# -*- coding: utf-8 -*-
# ------------------------------------------------------------------
# Enunciado 9:
# Escribí una función es_bisiesto(año) que devuelva True o False
# según la regla clásica:
# divisible por 4, salvo divisible por 100 excepto también por 400.
# ------------------------------------------------------------------


def es_bisiesto(año):
    return (año % 4 == 0 and año % 100 != 0) or año % 400 == 0


print(es_bisiesto(2024))
print(es_bisiesto(2023))
print(es_bisiesto(2100))
print(es_bisiesto(1600))
