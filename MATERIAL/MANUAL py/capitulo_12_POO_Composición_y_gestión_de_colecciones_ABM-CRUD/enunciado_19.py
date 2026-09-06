# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Composición más herencia: hacé Producto con nombre y precio_final(),
# y ProductoConDescuento(Producto) que sobrescriba precio_final().
# Después hacé Compra, que contiene una lista de productos y un método
# factura() que imprima cada línea y el total. Compra no debe preguntar
# de qué tipo es cada producto: le pide precio_final() a todos por
# igual y el polimorfismo hace el resto.
# -------------------------------------------------------------------------

class Producto:
    """Producto cuyo precio final es su precio de lista."""

    def __init__(self, nombre, precio):
        self._nombre = nombre
        self._precio = precio

    def nombre(self):
        """Devuelve el nombre del producto."""
        return self._nombre

    def precio_final(self):
        """Precio a cobrar por una unidad."""
        return self._precio


class ProductoConDescuento(Producto):
    """Producto cuyo precio final aplica un descuento."""

    def __init__(self, nombre, precio, descuento):
        super().__init__(nombre, precio)
        self._descuento = descuento

    def precio_final(self):
        return self._precio * (1 - self._descuento / 100)


class Compra:
    """Compra que factura sus productos polimórficamente."""

    def __init__(self):
        self._productos = []

    def agregar(self, producto):
        """Suma un producto a la compra."""
        self._productos.append(producto)

    def total(self):
        """Suma los precios finales de todos los productos."""
        return sum(
            producto.precio_final()
            for producto in self._productos
        )

    def factura(self):
        """Imprime el detalle de la compra y su total."""
        print("=== FACTURA ===")

        for producto in self._productos:
            print(
                f"  {producto.nombre()}: "
                f"${producto.precio_final():.2f}"
            )

        print(f"TOTAL: ${self.total():.2f}")


if __name__ == "__main__":
    compra = Compra()
    compra.agregar(Producto("Yerba", 3500))
    compra.agregar(ProductoConDescuento("Leche", 800, 20))
    compra.agregar(Producto("Pan", 1200))

    compra.factura()
