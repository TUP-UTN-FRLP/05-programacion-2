# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Ejercicio 1
# Reescribí este código para que use try/except en vez de isdigit().
# Debe aceptar negativos.
# -------------------------------------------------------------------------

entrada = input("Número: ")
# int() falla con ValueError si la entrada no es un número entero válido.
# El except captura ese error e imprime un mensaje sin cortar el programa.
try:
    numero = int(entrada)
    print(f"El doble es {numero * 2}")
except ValueError:
    print("No es un número")
