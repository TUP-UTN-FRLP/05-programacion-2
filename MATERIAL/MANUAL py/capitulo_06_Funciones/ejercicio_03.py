# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Escribí una función calcular_precio(base, iva=21, descuento=0) que devuelva
# el precio final aplicando primero el IVA y después el descuento
# (ambos en porcentaje).
# -----------------------------------------------------------------------------


def calcular_precio(base, iva=21, descuento=0):
    con_iva = base * (1 + iva / 100)
    final = con_iva * (1 - descuento / 100)
    return final


print(f"${calcular_precio(1000):.2f}")
print(f"${calcular_precio(1000, descuento=15):.2f}")
print(f"${calcular_precio(1000, iva=10.5, descuento=5):.2f}")
