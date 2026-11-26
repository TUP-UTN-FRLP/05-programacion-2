# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 1
# Pedile al usuario un número entero. Si ingresa cualquier otra cosa,
# mostrar "Entrada inválida" y no cortar el programa.
# -------------------------------------------------------------------------


# int() falla con ValueError si el usuario ingresa texto o un decimal.
# El except evita que el programa se corte y muestra "Entrada inválida".
try:
    numero = int(input("Número entero: "))
    print(f"Ingresaste {numero}")
except ValueError:
    print("Entrada inválida")
