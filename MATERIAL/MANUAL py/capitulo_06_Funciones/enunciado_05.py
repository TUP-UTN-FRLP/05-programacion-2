# -*- coding: utf-8 -*-
# ------------------------------------------------------------------
# Enunciado 5:
# Escribí una función es_primo(n) que devuelva True si n es primo
# y False si no.
# Usala para imprimir todos los primos entre 2 y 50.
#
# NOTA: En las versiones B y C se mide el tiempo de ejecución del
# programa para comparar la eficiencia de las funciones es_primo(n).
# ------------------------------------------------------------------


def es_primo(n):
    if n < 2:
        return False

    for divisor in range(2, n):
        if n % divisor == 0:
            return False

    return True


for numero in range(2, 51):
    if es_primo(numero):
        print(numero, end=" ")
