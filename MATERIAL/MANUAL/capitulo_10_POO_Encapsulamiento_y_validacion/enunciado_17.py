# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Ampliá la clase Producto para llevar un contador privado
# _ventas_totales (cantidad total vendida en unidades). Property de solo
# lectura. vender() lo actualiza.
# -------------------------------------------------------------------------


class StockInsuficienteError(Exception):
    """Se lanza cuando no hay suficiente stock para vender."""

    pass


class Producto:
    def __init__(self, nombre, precio, stock=0):
        # Como ampliamos la clase Producto del ejercicio anterior,
        # conservamos sus validaciones.
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")

        self._nombre = nombre.strip()

        # Usamos las properties para que precio y stock pasen por sus
        # setters también durante la creación del objeto.
        self.precio = precio
        self.stock = stock

        # _ventas_totales comienza siempre en cero.
        #
        # No recibimos este valor como argumento porque representa un
        # dato que debe controlar exclusivamente la propia clase.
        self._ventas_totales = 0

    @property
    def nombre(self):
        # nombre es una property de solo lectura.
        return self._nombre

    @property
    def precio(self):
        return self._precio

    @precio.setter
    def precio(self, valor):
        if type(valor) not in (int, float):
            raise TypeError("El precio debe ser numérico")

        if valor < 0:
            raise ValueError("El precio no puede ser negativo")

        self._precio = valor

    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, valor):
        # El stock representa unidades completas.
        if type(valor) is not int:
            raise TypeError("El stock debe ser un número entero")

        if valor < 0:
            raise ValueError("El stock no puede ser negativo")

        self._stock = valor

    @property
    def ventas_totales(self):
        # ventas_totales es una property de solo lectura.
        #
        # Como no existe @ventas_totales.setter, el valor puede
        # consultarse desde afuera pero no asignarse directamente.
        return self._ventas_totales

    def vender(self, cantidad):
        # Secuencia:
        # vender(cantidad)
        #         ↓
        # validar que sea un entero
        #         ↓
        # validar que sea positiva
        #         ↓
        # verificar que exista stock suficiente
        #         ↓
        # descontar del stock
        #         ↓
        # aumentar _ventas_totales

        if type(cantidad) is not int:
            raise TypeError("La cantidad debe ser un número entero")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")

        if cantidad > self._stock:
            raise StockInsuficienteError(
                f"Se intentaron vender {cantidad} "
                f"pero solo hay {self._stock}"
            )

        # Calculamos el nuevo stock y lo asignamos mediante la property.
        # Así la modificación vuelve a pasar por el setter.
        nuevo_stock = self._stock - cantidad
        self.stock = nuevo_stock

        # _ventas_totales se modifica directamente desde la clase.
        #
        # Usamos un solo guion bajo porque en Python indica, por
        # convención, que el atributo es de uso interno.
        #
        # No usamos __ventas_totales porque el doble guion bajo activa
        # name mangling, usado principalmente para evitar colisiones de
        # nombres en situaciones de herencia.
        self._ventas_totales += cantidad


# ---------------------------------------------------------------
# CASO 1: creación del producto
#
# Producto("Yerba", 3500, 20)
#         ↓
# stock = 20
# ventas_totales = 0
# ---------------------------------------------------------------

producto = Producto("Yerba", 3500, 20)

print(f"Producto: {producto.nombre}")
print(f"Precio: ${producto.precio:.2f}")
print(f"Stock: {producto.stock}")
print(f"Ventas totales: {producto.ventas_totales}")


# ---------------------------------------------------------------
# CASO 2: primera venta
#
# vender(5)
#         ↓
# stock: 20 - 5 = 15
#         ↓
# ventas_totales: 0 + 5 = 5
# ---------------------------------------------------------------

producto.vender(5)

print(f"Stock: {producto.stock}")  # 15
print(f"Ventas totales: {producto.ventas_totales}")  # 5


# ---------------------------------------------------------------
# CASO 3: segunda venta
#
# vender(3)
#         ↓
# stock: 15 - 3 = 12
#         ↓
# ventas_totales: 5 + 3 = 8
# ---------------------------------------------------------------

producto.vender(3)

print(f"Stock: {producto.stock}")  # 12
print(f"Ventas totales: {producto.ventas_totales}")  # 8


# ---------------------------------------------------------------
# CASO 4: intento de modificar ventas_totales desde afuera
#
# producto.ventas_totales = 100
#         ↓
# Python busca @ventas_totales.setter
#         ↓
# no existe
#         ↓
# AttributeError
# ---------------------------------------------------------------

try:
    producto.ventas_totales = 100
except AttributeError as error:
    print(f"Error: {error}")


# El contador conserva el valor administrado por la propia clase.
print(f"Ventas totales: {producto.ventas_totales}")  # 8


# ---------------------------------------------------------------
# CASO 5: intento de vender más unidades que las disponibles
#
# vender(100)
#         ↓
# 100 > 12
#         ↓
# StockInsuficienteError
# ---------------------------------------------------------------

try:
    producto.vender(100)
except StockInsuficienteError as error:
    print(f"Error: {error}")


# Una venta rechazada no modifica ni el stock ni ventas_totales.
print(f"Stock: {producto.stock}")  # 12
print(f"Ventas totales: {producto.ventas_totales}")  # 8


# ---------------------------------------------------------------
# CASO 6: intento de vender una cantidad negativa
# ---------------------------------------------------------------

try:
    producto.vender(-2)
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 7: intento de vender una cantidad con decimales
# ---------------------------------------------------------------

try:
    producto.vender(2.5)
except TypeError as error:
    print(f"Error: {error}")
