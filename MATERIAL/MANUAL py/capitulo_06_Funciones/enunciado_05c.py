# -*- coding: utf-8 -*-
# --------------------------------------------------------------------------
# Enunciado 5: (versión optimizada)
# Escribí una función es_primo(n) que devuelva True si n es primo
# y False si no.
# Usala para imprimir todos los primos entre 2 y 50.
#
# NOTA: Este código es una versión optimizada de la función es_primo(n)
#       que reduce la cantidad de divisiones necesarias para determinar
#       si un número es primo. En lugar de probar todos los números desde
#       2 hasta n-1, solo se prueban los divisores hasta la raíz cuadrada
#       de n y se omiten los números pares después del 2.
#
# IMPORTACIONES: Se importa el módulo math para utilizar la función isqrt()
#                que calcula la raíz cuadrada entera de un número.
#                Se importa el módulo time para medir el tiempo de ejecución
#                del programa.
#
# INSTRUCCIONES: Compara con 100001 para comparar optimización con relación
#                a la versión B.
# --------------------------------------------------------------------------

import math
import time

tiempo_inicial = time.time()


def es_primo(n):
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    # Probar solo divisores impares hasta √n
    limite = math.isqrt(n)
    for divisor in range(3, limite + 1, 2):
        if n % divisor == 0:
            return False

    return True


for numero in range(2, 1000001):
    if es_primo(numero):
        print(numero, end=" ")

print()
tiempo_final = time.time()
print(f"Tiempo de ejecución: {tiempo_final - tiempo_inicial} segundos")
