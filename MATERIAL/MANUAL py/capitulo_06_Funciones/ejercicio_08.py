# -*- coding: utf-8 -*-
# ------------------------------------------------------------------------
# Agregá un docstring a la función calcular_precio que escribiste antes,
# y probá help(calcular_precio) en el shell.
# ------------------------------------------------------------------------


def calcular_precio(base, iva=21, descuento=0):
    """Calcula el precio final aplicando IVA y luego descuento.

    base: precio sin impuestos
    iva: porcentaje de IVA (por defecto 21)
    descuento: porcentaje de descuento (por defecto 0)
    """
    con_iva = base * (1 + iva / 100)
    final = con_iva * (1 - descuento / 100)
    return final


help(calcular_precio)
