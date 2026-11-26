# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
# Enunciado 5:
# Escribí una función es_primo(n) que devuelva True si n es primo
# y False si no.
# Usala para imprimir todos los primos entre 2 y 50.
#
# IMPORTACIONES: Se importa el módulo time para medir el tiempo de ejecución
#                del programa.
#
# INSTRUCCIONES: Compara con 100001 para comparar versión optimizada C.
# --------------------------------------------------------------------------
import time

tiempo_inicial = time.time()


def es_primo(n):
    if n < 2:
        return False

    for divisor in range(2, n):
        if n % divisor == 0:
            return False

    return True


for numero in range(2, 1000001):
    if es_primo(numero):
        print(numero, end=" ")

print()
tiempo_final = time.time()
print(f"Tiempo de ejecución: {tiempo_final - tiempo_inicial} segundos")
