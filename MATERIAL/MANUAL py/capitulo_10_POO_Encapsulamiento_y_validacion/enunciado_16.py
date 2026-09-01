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
        # Primero validamos el nombre porque no tiene setter.
        #
        # Debe ser un string y no puede quedar vacío después de eliminar
        # los espacios de los extremos con strip().
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")

        # _nombre es un atributo interno de solo lectura.
        self._nombre = nombre.strip()

        # No guardamos directamente:
        # self._precio = precio
        # self._stock = stock
        #
        # Usamos las properties para que sus setters también validen los
        # valores durante la creación del objeto.
        #
        # Secuencia:
        # Producto(nombre, precio, stock)
        #         ↓
        # validar nombre
        #         ↓
        # self.precio = precio
        #         ↓
        # setter de precio
        #         ↓
        # self.stock = stock
        #         ↓
        # setter de stock
        self.precio = precio
        self.stock = stock

    @property
    def nombre(self):
        # nombre es una property de solo lectura porque no tiene setter.
        return self._nombre

    @property
    def precio(self):
        # precio es la property pública.
        # _precio es el atributo interno donde se guarda el valor.
        return self._precio

    @precio.setter
    def precio(self, valor):
        # El precio debe ser un número.
        if type(valor) not in (int, float):
            raise TypeError("El precio debe ser numérico")

        # Permitimos precio cero, pero no valores negativos.
        if valor < 0:
            raise ValueError("El precio no puede ser negativo")

        # El valor se guarda solamente después de superar las
        # validaciones.
        self._precio = valor

    @property
    def stock(self):
        # stock es la property pública.
        # _stock contiene la cantidad real disponible.
        return self._stock

    @stock.setter
    def stock(self, valor):
        # En este ejemplo el stock representa unidades completas, por lo
        # que solamente aceptamos números enteros.
        if type(valor) is not int:
            raise TypeError("El stock debe ser un número entero")

        if valor < 0:
            raise ValueError("El stock no puede ser negativo")

        # Usamos un solo guion bajo (_stock) porque en Python indica, por
        # convención, que el atributo es de uso interno de la clase.
        # Técnicamente puede accederse desde afuera, pero hacerlo
        # significa romper el contrato de la clase.
        #
        # No usamos __stock porque el doble guion bajo activa name
        # mangling, usado principalmente para evitar colisiones de
        # nombres en situaciones de herencia.
        self._stock = valor

    def vender(self, cantidad):
        # La cantidad a vender también debe representar unidades
        # completas.
        #
        # Secuencia:
        # vender(cantidad)
        #         ↓
        # validar que sea un entero
        #         ↓
        # validar que sea positiva
        #         ↓
        # verificar que exista stock suficiente
        #         ↓
        # descontar la cantidad del stock
        if type(cantidad) is not int:
            raise TypeError("La cantidad debe ser un número entero")

        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")

        # Si la cantidad es válida pero supera el stock disponible,
        # usamos una excepción específica del dominio.
        if cantidad > self._stock:
            raise StockInsuficienteError(
                f"Se intentaron vender {cantidad} "
                f"pero solo hay {self._stock}"
            )

        # Calculamos el nuevo stock.
        nuevo_stock = self._stock - cantidad

        # En lugar de modificar directamente:
        # self._stock = nuevo_stock
        #
        # usamos la property para mantener una única puerta de entrada
        # para las modificaciones del stock.
        self.stock = nuevo_stock


# ---------------------------------------------------------------
# CASO 1: creación de un producto válido
#
# Producto("Yerba", 3500, 20)
#         ↓
# nombre válido
#         ↓
# precio válido
#         ↓
# stock válido
# ---------------------------------------------------------------

producto = Producto("Yerba", 3500, 20)

print(f"Producto: {producto.nombre}")
print(f"Precio: ${producto.precio:.2f}")
print(f"Stock: {producto.stock}")


# ---------------------------------------------------------------
# CASO 2: venta válida
#
# vender(5)
#         ↓
# 5 es entero y positivo
#         ↓
# hay 20 unidades
#         ↓
# nuevo stock = 20 - 5
#         ↓
# stock = 15
# ---------------------------------------------------------------

producto.vender(5)

print(f"Stock después de vender 5 unidades: {producto.stock}")


# ---------------------------------------------------------------
# CASO 3: intento de vender más unidades que las disponibles
#
# vender(100)
#         ↓
# cantidad válida
#         ↓
# 100 > 15
#         ↓
# StockInsuficienteError
# ---------------------------------------------------------------

try:
    producto.vender(100)
except StockInsuficienteError as error:
    print(f"Error: {error}")


# La venta rechazada no modifica el stock.
print(f"Stock actual: {producto.stock}")


# ---------------------------------------------------------------
# CASO 4: cantidad de venta negativa
# ---------------------------------------------------------------

try:
    producto.vender(-2)
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 5: cantidad de venta con decimales
# ---------------------------------------------------------------

try:
    producto.vender(2.5)
except TypeError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 6: intento de asignar un precio negativo
#
# producto.precio = -100
#         ↓
# setter de precio
#         ↓
# ValueError
# ---------------------------------------------------------------

try:
    producto.precio = -100
except ValueError as error:
    print(f"Error: {error}")


# El precio anterior se conserva.
print(f"Precio actual: ${producto.precio:.2f}")


# ---------------------------------------------------------------
# CASO 7: intento de asignar stock negativo
# ---------------------------------------------------------------

try:
    producto.stock = -10
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 8: creación de un producto inválido
#
# Como __init__ utiliza los setters, las mismas reglas también se
# aplican durante la creación del objeto.
# ---------------------------------------------------------------

try:
    producto_invalido = Producto("Azúcar", -500, 10)
except ValueError as error:
    print(f"Error: {error}")
