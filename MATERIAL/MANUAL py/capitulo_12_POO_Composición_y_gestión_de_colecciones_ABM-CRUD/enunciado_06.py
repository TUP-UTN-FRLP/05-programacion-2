# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé un Carrito de compras con tres clases: Producto, con nombre y
# precio; LineaDeCarrito, que junta un Producto con una cantidad y sabe
# calcular su subtotal; y Carrito, que contiene una lista de líneas.
# Agregá agregar(producto, cantidad), total() y mostrar(). Fijate que
# cada clase calcula lo suyo y le pide el resto a la de abajo.
# -------------------------------------------------------------------------

class Producto:
    """Producto con nombre y precio unitario."""

    def __init__(self, nombre, precio):
        self._nombre = nombre
        self._precio = precio

    def nombre(self):
        """Devuelve el nombre del producto."""
        return self._nombre

    def precio(self):
        """Devuelve el precio unitario."""
        return self._precio

    def __str__(self):
        return f"{self._nombre} (${self._precio})"


class LineaDeCarrito:
    """Una línea del carrito: un producto y su cantidad."""

    def __init__(self, producto, cantidad):
        self._producto = producto
        self._cantidad = cantidad

    def subtotal(self):
        """Precio unitario por la cantidad pedida."""
        return self._producto.precio() * self._cantidad

    def __str__(self):
        return (
            f"{self._producto.nombre()} x{self._cantidad}: "
            f"${self.subtotal()}"
        )


class Carrito:
    """Carrito compuesto por líneas de compra."""

    def __init__(self):
        self._lineas = []

    def agregar(self, producto, cantidad):
        """Suma una línea nueva al carrito."""
        self._lineas.append(
            LineaDeCarrito(producto, cantidad)
        )

    def total(self):
        """Suma los subtotales de todas las líneas."""
        return sum(
            linea.subtotal() for linea in self._lineas
        )

    def mostrar(self):
        """Imprime el detalle del carrito y su total."""
        for linea in self._lineas:
            print(f"  {linea}")

        print(f"  TOTAL: ${self.total()}")


if __name__ == "__main__":
    carrito = Carrito()
    carrito.agregar(Producto("Yerba", 3500), 2)
    carrito.agregar(Producto("Leche", 800), 3)

    carrito.mostrar()
