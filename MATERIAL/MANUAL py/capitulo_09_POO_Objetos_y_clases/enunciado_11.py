# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 11
# Definí una clase Producto con nombre, precio_unitario y stock.
# Agregale un método valor_stock() que devuelva
# precio_unitario * stock.
# -------------------------------------------------------------------------


class Producto:

    def __init__(self, nombre, precio_unitario, stock):
        self.nombre = nombre
        self.precio_unitario = precio_unitario
        self.stock = stock

    def valor_stock(self):
        return self.precio_unitario * self.stock


yerba = Producto("Yerba Playadito", 3500, 20)

print(f"Valor total del stock: ${yerba.valor_stock()}")
