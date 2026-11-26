# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Producto con nombre y precio_final(), que devuelve el
# precio. Definí ProductoConDescuento(Producto) que sobrescribe
# precio_final() restando un porcentaje. Después hacé una clase Tienda
# con nombre, un método agregar(producto) y un método precio_total()
# que sume los precios finales. Tienda debe llamar a precio_final()
# polimórficamente, sin preguntar de qué tipo es cada producto.
# -------------------------------------------------------------------------

class Producto:
    """Producto cuyo precio final es igual a su precio de lista."""

    def __init__(self, nombre, precio):
        self._nombre = nombre
        self._precio = precio

    def precio_final(self):
        """Precio a cobrar por una unidad."""
        return self._precio

    def __str__(self):
        return f"  {self._nombre}: ${self.precio_final():.2f}"


class ProductoConDescuento(Producto):
    """Producto cuyo precio final aplica un descuento porcentual."""

    def __init__(self, nombre, precio, descuento):
        super().__init__(nombre, precio)
        self._descuento = descuento

    def precio_final(self):
        return self._precio * (1 - self._descuento / 100)


class Tienda:
    """Tienda que suma precios finales polimórficamente."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._productos = []

    def agregar(self, producto):
        """Suma un producto al catálogo de la tienda."""
        self._productos.append(producto)

    def precio_total(self):
        """Devuelve la suma de los precios finales del catálogo."""
        return sum(
            producto.precio_final()
            for producto in self._productos
        )

    def listar(self):
        """Imprime el catálogo y el total a cobrar."""
        print(f"{self._nombre}")
        for producto in self._productos:
            print(producto)
        print(f"  Total: ${self.precio_total():.2f}")


tienda = Tienda("Almacén")
tienda.agregar(Producto("Pan", 500))
tienda.agregar(ProductoConDescuento("Yerba", 3500, 20))
tienda.agregar(Producto("Leche", 800))

tienda.listar()
