# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Sistema con dos gestores adentro: RegistroUsuarios y
# RegistroProductos, cada uno con su propio ABM chico. Sistema no
# guarda usuarios ni productos: los delega. Exponé crear_usuario(),
# crear_producto() y resumen(), que imprime los totales de cada uno.
# Cada registro guarda objetos, no diccionarios sueltos: si el dato
# tiene identidad y comportamiento, merece una clase.
# -------------------------------------------------------------------------

class Usuario:
    """Usuario identificado por su email."""

    def __init__(self, email, nombre):
        self._email = email
        self._nombre = nombre

    def __str__(self):
        return f"{self._nombre} <{self._email}>"


class Producto:
    """Producto identificado por su código."""

    def __init__(self, codigo, nombre, precio):
        self._codigo = codigo
        self._nombre = nombre
        self._precio = precio

    def __str__(self):
        return f"[{self._codigo}] {self._nombre} ${self._precio}"


class RegistroUsuarios:
    """Registro de usuarios indexados por email."""

    def __init__(self):
        self._usuarios = {}

    def crear(self, email, nombre):
        """Da de alta un usuario y lo devuelve."""
        usuario = Usuario(email, nombre)
        self._usuarios[email] = usuario

        return usuario

    def cantidad(self):
        """Cuántos usuarios hay registrados."""
        return len(self._usuarios)

    def listar(self):
        """Devuelve todos los usuarios."""
        return list(self._usuarios.values())


class RegistroProductos:
    """Registro de productos indexados por código."""

    def __init__(self):
        self._productos = {}

    def crear(self, codigo, nombre, precio):
        """Da de alta un producto y lo devuelve."""
        producto = Producto(codigo, nombre, precio)
        self._productos[codigo] = producto

        return producto

    def cantidad(self):
        """Cuántos productos hay registrados."""
        return len(self._productos)

    def listar(self):
        """Devuelve todos los productos."""
        return list(self._productos.values())


class Sistema:
    """Sistema compuesto por dos registros independientes."""

    def __init__(self):
        self._usuarios = RegistroUsuarios()
        self._productos = RegistroProductos()

    def crear_usuario(self, email, nombre):
        """Delega el alta en el registro de usuarios."""
        return self._usuarios.crear(email, nombre)

    def crear_producto(self, codigo, nombre, precio):
        """Delega el alta en el registro de productos."""
        return self._productos.crear(codigo, nombre, precio)

    def resumen(self):
        """Imprime los totales de cada registro."""
        print(f"Usuarios:  {self._usuarios.cantidad()}")

        for usuario in self._usuarios.listar():
            print(f"  {usuario}")

        print(f"Productos: {self._productos.cantidad()}")

        for producto in self._productos.listar():
            print(f"  {producto}")


if __name__ == "__main__":
    sistema = Sistema()
    sistema.crear_usuario("ana@correo.com", "Ana")
    sistema.crear_usuario("juan@correo.com", "Juan")
    sistema.crear_producto("P-001", "Yerba", 3500)

    sistema.resumen()
