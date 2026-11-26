# -*- coding: utf-8 -*-
# ------------------------------------------------------
# Enunciado 11:
# Escribí una función descuento(precio, porcentaje=10)
# que devuelva el precio con descuento aplicado.
# ------------------------------------------------------


def descuento(precio, porcentaje=10):
    return precio * (1 - porcentaje / 100)


print(descuento(1000))
print(descuento(1000, 25))
print(f"{descuento(1000, porcentaje=50):.2f}")
