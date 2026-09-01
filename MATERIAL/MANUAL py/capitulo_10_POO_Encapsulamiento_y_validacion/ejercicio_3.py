# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Creá una clase Producto con nombre (string no vacío), precio (número
# positivo, cero incluido) y stock (entero mayor o igual a cero).
#
# Validá todo en el __init__.
#
# Además, precio y stock deben ser properties con setters que también
# validen.
#
# Mantener las validaciones de tipo y valor presentadas en el capítulo y
# las pruebas correspondientes.
# -------------------------------------------------------------------------


class Producto:
    def __init__(self, nombre, precio, stock):
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValueError("El nombre debe ser un string no vacío")
        self.nombre = nombre
        self.precio = precio        # pasa por el setter (valida)
        self.stock = stock          # pasa por el setter (valida)

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


p = Producto("Yerba", 3000, 10)
print(p.nombre, p.precio, p.stock)

p.precio = 0                    # cero incluido: es válido
print(p.precio)

# Cada entrada inválida debe frenarse con TypeError o ValueError.
invalidas = [
    ("", 100, 1),
    ("Pan", -1, 1),
    ("Pan", 100, -1),
    ("Pan", "cara", 1),
    ("Pan", 100, 1.5),
]
for datos in invalidas:
    try:
        Producto(*datos)
    except (TypeError, ValueError) as e:
        print("Error:", e)
