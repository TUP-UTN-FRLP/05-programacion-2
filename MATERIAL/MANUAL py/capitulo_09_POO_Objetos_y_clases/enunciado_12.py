# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 12
# Sumale a Producto un método vender(cantidad) que reste cantidad del
# stock. Por ahora sin validar, solo resta.
# -------------------------------------------------------------------------


class Producto:

    def __init__(self, nombre, precio_unitario, stock):
        self.nombre = nombre
        self.precio_unitario = precio_unitario
        self.stock = stock

    def valor_stock(self):
        return self.precio_unitario * self.stock

    def vender(self, cantidad):
        self.stock -= cantidad


yerba = Producto("Yerba Playadito", 3500, 20)

yerba.vender(3)

print(yerba.stock)

yerba.vender(100)

print(yerba.stock)
