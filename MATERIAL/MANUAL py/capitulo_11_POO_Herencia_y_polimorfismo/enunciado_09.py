# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Producto con nombre, precio y un método precio_final()
# que devuelve el precio. Hacé ProductoConIVA(Producto) que sobrescriba
# precio_final() agregando 21% de IVA, y ProductoImportado que agregue
# un 15% de arancel sobre el anterior. Fijate cómo cada super() encadena
# con el nivel inmediatamente superior.
#
# Ojo con el diseño: la prueba del "es un" acá no se sostiene del todo.
# Un producto importado no "es un" producto con IVA: el IVA es una regla
# fiscal, no un tipo de producto. Sirve para ver super() en cadena, pero
# en el capítulo 12 vamos a modelarlo mejor con composición.
# -------------------------------------------------------------------------

class Producto:
    """Producto con precio base."""

    def __init__(self, nombre, precio):
        self._nombre = nombre
        self._precio = precio

    def precio_final(self):
        """Precio sin recargos."""
        return self._precio

    def __str__(self):
        return f"{self._nombre}: ${self.precio_final():.2f}"


class ProductoConIVA(Producto):
    """Producto que agrega 21 por ciento de IVA."""

    def precio_final(self):
        return super().precio_final() * 1.21


class ProductoImportado(ProductoConIVA):
    """Producto que agrega un arancel sobre el precio con IVA."""

    def precio_final(self):
        return super().precio_final() * 1.15


producto = Producto("Yerba", 3000)
producto_iva = ProductoConIVA("Bebida", 3000)
importado = ProductoImportado("Whisky", 3000)

print(producto)
print(producto_iva)
print(importado)
