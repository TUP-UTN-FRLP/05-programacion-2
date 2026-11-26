# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Enunciado 17:
# Escribí una función es_palindromo(texto) que devuelva True
# si el texto se lee igual al derecho y al revés.
# Debe ignorar mayúsculas y espacios.
# ------------------------------------------------------------


def es_palindromo(texto):
    limpio = texto.lower().replace(" ", "")

    return limpio == limpio[::-1]


print(es_palindromo("Anita lava la tina"))
print(es_palindromo("Python"))
print(es_palindromo("Reconocer"))
