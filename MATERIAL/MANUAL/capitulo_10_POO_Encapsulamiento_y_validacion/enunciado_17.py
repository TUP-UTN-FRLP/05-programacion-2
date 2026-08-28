# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Ampliá la clase Producto para llevar un contador privado
# _ventas_totales (cantidad total vendida en unidades). Property de solo
# lectura. vender() lo actualiza.
# -------------------------------------------------------------------------


class Producto:
    def __init__(self, nombre, precio, stock=0):
        self._nombre = nombre.strip()
        self._precio = precio
        self._stock = stock
        self._ventas_totales = 0

    @property
    def ventas_totales(self):
        return self._ventas_totales

    def vender(self, cantidad):
        if cantidad > self._stock:
            raise StockInsuficienteError("Stock insuficiente")

        self._stock -= cantidad
        self._ventas_totales += cantidad


p = Producto("Yerba", 3500, 20)

p.vender(5)
p.vender(3)

print(p.ventas_totales)  # 8

p.ventas_totales = 100  # AttributeError (solo lectura)
