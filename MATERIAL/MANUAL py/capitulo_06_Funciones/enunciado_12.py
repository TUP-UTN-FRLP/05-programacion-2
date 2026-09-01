# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Enunciado 12:
# Escribí una función frecuencia(texto) que devuelva un diccionario
# con la frecuencia de cada palabra en el texto.
# -------------------------------------------------------------------


def frecuencia(texto):
    resultado = {}

    for palabra in texto.lower().split():
        resultado[palabra] = resultado.get(palabra, 0) + 1

    return resultado


print(frecuencia("el gato y el perro y el ratón"))
