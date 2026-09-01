# -*- coding: utf-8 -*-
# -----------------------------------------------------------------
# Enunciado 10:
# Escribí una función imc(peso, altura) que devuelva una tupla
# (imc, categoría).
# La categoría debe ser "bajo", "normal", "sobrepeso" u "obesidad"
# según los rangos habituales.
# -----------------------------------------------------------------


def imc(peso, altura):
    valor = peso / (altura ** 2)

    if valor < 18.5:
        categoria = "bajo"
    elif valor < 25:
        categoria = "normal"
    elif valor < 30:
        categoria = "sobrepeso"
    else:
        categoria = "obesidad"

    return valor, categoria


valor, cat = imc(70, 1.75)

print(f"IMC: {valor:.2f} - {cat}")
