# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Implementá un gestor de productos con ABM completo. Cada Producto
# tiene codigo, nombre, precio y stock. Usá un diccionario interno en
# Almacen, con alta, consulta, listado, actualización de precio,
# reposición de stock y baja. Creá excepciones propias para código
# duplicado y producto no encontrado, y reutilizá buscar() dentro de
# los métodos que necesitan encontrar un producto.
# -------------------------------------------------------------------------

class ProductoNoEncontrado(Exception):
    """Indica que no existe el producto solicitado."""

    pass


class CodigoDuplicadoError(Exception):
    """Indica que el código del producto ya existe."""

    pass


class Producto:
    """Producto identificado por un código."""

    def __init__(self, codigo, nombre, precio, stock):
        self._codigo = codigo
        self._nombre = nombre
        self._precio = precio
        self._stock = stock

    def cambiar_precio(self, nuevo_precio):
        """Actualiza el precio de venta."""
        if nuevo_precio <= 0:
            raise ValueError("El precio debe ser positivo")

        self._precio = nuevo_precio

    def reponer(self, cantidad):
        """Suma unidades al stock disponible."""
        if cantidad <= 0:
            raise ValueError("La cantidad debe ser positiva")

        self._stock += cantidad

    def __str__(self):
        return (
            f"[{self._codigo}] {self._nombre} - "
            f"${self._precio} (stock: {self._stock})"
        )


class Almacen:
    """Gestiona un ABM de productos indexados por código."""

    def __init__(self):
        self._productos = {}

    def dar_de_alta(self, codigo, nombre, precio, stock):
        """Da de alta un producto nuevo y lo devuelve."""
        if codigo in self._productos:
            raise CodigoDuplicadoError(
                f"Ya existe un producto con código {codigo}"
            )

        producto = Producto(codigo, nombre, precio, stock)
        self._productos[codigo] = producto

        return producto

    def buscar(self, codigo):
        """Devuelve el producto pedido o lanza excepción."""
        producto = self._productos.get(codigo)

        if producto is None:
            raise ProductoNoEncontrado(
                f"No existe el código {codigo}"
            )

        return producto

    def listar(self):
        """Devuelve todos los productos del almacén."""
        return list(self._productos.values())

    def actualizar_precio(self, codigo, nuevo_precio):
        """Le pide al producto que cambie su precio."""
        self.buscar(codigo).cambiar_precio(nuevo_precio)

    def reponer_stock(self, codigo, cantidad):
        """Le pide al producto que sume stock."""
        self.buscar(codigo).reponer(cantidad)

    def dar_de_baja(self, codigo):
        """Elimina físicamente el producto indicado."""
        self.buscar(codigo)
        del self._productos[codigo]


if __name__ == "__main__":
    almacen = Almacen()
    almacen.dar_de_alta("P-001", "Yerba", 3500, 20)
    almacen.dar_de_alta("P-002", "Leche", 800, 15)

    almacen.actualizar_precio("P-001", 4000)
    almacen.reponer_stock("P-001", 10)
    almacen.dar_de_baja("P-002")

    for producto in almacen.listar():
        print(producto)

    try:
        almacen.dar_de_alta("P-001", "Otra yerba", 3000, 5)
    except CodigoDuplicadoError as error:
        print(f"Error: {error}")

    try:
        almacen.buscar("P-002")
    except ProductoNoEncontrado as error:
        print(f"Error: {error}")
