# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 7
# Un programa que insista al usuario hasta que ingrese un número
# válido: usá un while True y un break dentro del else del try.
# -------------------------------------------------------------------------


while True:
    # int() falla con ValueError si la entrada no es un número entero.
    # El except muestra el error y vuelve a pedir; el else corta el bucle.
    try:
        numero = int(input("Número: "))
    except ValueError:
        print("Eso no es un número, probá de nuevo")
    else:
        break


print(f"Perfecto, ingresaste {numero}")
