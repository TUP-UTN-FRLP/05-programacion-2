# -*- coding: utf-8 -*-
# -----------------------------------------------------------------
# Escribí es_par(n) que devuelva True o False (sin imprimir nada).
# Después usala en un if para decidir qué imprimir.
#
# PREGUNTA: ¿Por qué el retorno de la función es_par() es True o
# False?
#
# -----------------------------------------------------------------

def es_par(n):
    return n % 2 == 0


numero = input("Número: ")

while not numero.isdigit():
    print("Error: Debe ingresar un número entero.")
    numero = input("Número: ")

numero = int(numero)

if es_par(numero):
    print(f"{numero} es par")
else:
    print(f"{numero} es impar")
