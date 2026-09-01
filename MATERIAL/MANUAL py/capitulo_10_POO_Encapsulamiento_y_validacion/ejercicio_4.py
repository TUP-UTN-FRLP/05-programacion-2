# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Creá una excepción StockInsuficienteError.
#
# Después modificá la clase Producto del ejercicio anterior para que tenga
# un método vender(cantidad) que reste del stock si hay suficiente, o lance
# la excepción si no.
#
# Probá los dos casos.
#
# Este archivo debe ser autocontenido: no debe depender de ejecutar
# ejercicio_3.py.
#
# Por lo tanto, incluir en ejercicio_4.py las definiciones necesarias de
# StockInsuficienteError y Producto.
# -------------------------------------------------------------------------


class StockInsuficienteError(Exception):
    pass


class Producto:
    def __init__(self, nombre, precio, stock):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre debe ser un string no vacío")
        self.nombre = nombre
        self.precio = precio
        self.stock = stock

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if not isinstance(valor, (int, float)):
            raise TypeError("El precio debe ser un número")
        if valor < 0:
            raise ValueError("El precio no puede ser negativo")
        self._precio = valor

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        if not isinstance(valor, int):
            raise TypeError("El stock debe ser un entero")
        if valor < 0:
            raise ValueError("El stock no puede ser negativo")
        self._stock = valor

    def vender(self, cantidad):
        if cantidad > self.stock:
            raise StockInsuficienteError(
                f"Hay {self.stock} unidades y se pidieron {cantidad}"
            )
        self.stock -= cantidad
        return self.stock


p = Producto("Yerba", 3000, 10)

# Caso 1: hay stock suficiente.
p.vender(4)
print(p.stock)                  # 6

# Caso 2: no hay stock suficiente -> lanza la excepción.
try:
    p.vender(20)
except StockInsuficienteError as e:
    print("Error:", e)
