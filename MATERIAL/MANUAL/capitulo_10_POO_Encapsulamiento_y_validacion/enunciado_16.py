# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Producto con nombre, precio y stock, todos con
# validación. Agregale un método vender(cantidad) que reste del stock,
# lanzando StockInsuficienteError si no hay suficiente.
# -------------------------------------------------------------------------


class StockInsuficienteError(Exception):
    """Se lanza cuando no hay suficiente stock para vender."""

    pass


class Producto:
    def __init__(self, nombre, precio, stock=0):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")

        self._nombre = nombre.strip()
        self.precio = precio
        self.stock = stock

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if valor < 0:
            raise ValueError("El precio no puede ser negativo")

        self._precio = valor

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        if valor < 0:
            raise ValueError("El stock no puede ser negativo")

        self._stock = valor

    def vender(self, cantidad):
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")

        if cantidad > self._stock:
            raise StockInsuficienteError(
                f"Se intentaron vender {cantidad} "
                f"pero solo hay {self._stock}"
            )

        self._stock -= cantidad


p = Producto("Yerba", 3500, 20)

p.vender(5)  # OK

p.vender(100)  # StockInsuficienteError
