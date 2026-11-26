# -*- coding: utf-8 -*-
# --------------------------------------------------------
# Enunciado 7:
# Escribí una función contar_vocales(texto) que devuelva
# cuántas vocales tiene un string.
# --------------------------------------------------------


def contar_vocales(texto):
    contador = 0

    for letra in texto.lower():
        if letra in "aeiouáéíóú":
            contador += 1

    return contador


print(contar_vocales("Hola Mundo"))
print(contar_vocales("Pythón"))
