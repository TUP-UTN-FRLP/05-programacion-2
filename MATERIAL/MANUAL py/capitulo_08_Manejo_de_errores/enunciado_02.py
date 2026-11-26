# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 2
# Pedile dos números y mostrar la división. Manejar por separado el
# caso de entrada no numérica y el de división por cero.
# -------------------------------------------------------------------------


# float() falla con ValueError si la entrada no es numérica.
# a / b falla con ZeroDivisionError si b es cero.
# Cada except captura un tipo distinto de error con su propio mensaje.
try:
    a = float(input("Numerador: "))
    b = float(input("Denominador: "))
    print(f"Resultado: {a / b}")
except ValueError:
    print("Los números deben ser válidos")
except ZeroDivisionError:
    print("No se puede dividir por cero")
