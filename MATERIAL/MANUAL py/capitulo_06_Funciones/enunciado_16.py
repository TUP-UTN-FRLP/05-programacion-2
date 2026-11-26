# -*- coding: utf-8 -*-
# -------------------------------------------------------------
# Enunciado 16:
# Escribí una función aplicar_iva(precios, iva=21) que reciba
# un diccionario de precios y devuelva un diccionario nuevo
# con los precios con IVA aplicado.
#
# Ejemplo:
# aplicar_iva({"pan": 500, "leche": 800})
# -> {"pan": 605.0, "leche": 968.0}
# -------------------------------------------------------------


def aplicar_iva(precios, iva=21):
    resultado = {}

    for producto, precio in precios.items():
        resultado[producto] = precio * (1 + iva / 100)

    return resultado


precios = {
    "pan": 500,
    "leche": 800,
    "yerba": 3000
}

print(aplicar_iva(precios))
print(aplicar_iva(precios, 10.5))
