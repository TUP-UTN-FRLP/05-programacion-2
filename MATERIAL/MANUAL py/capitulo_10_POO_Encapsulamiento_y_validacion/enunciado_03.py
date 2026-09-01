# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Convertí la clase Punto del capítulo anterior para que x e y sean
# privados y expuestos como properties de solo lectura. El único modo de
# "cambiarlos" es crear un nuevo Punto.
# -------------------------------------------------------------------------


class Punto:
    def __init__(self, x, y):
        # Como x e y serán properties de solo lectura, no tendrán
        # setters. Por eso la validación se realiza directamente en el
        # constructor.
        #
        # Secuencia:
        #
        # Punto(x, y)
        #     ↓
        # __init__()
        #     ↓
        # validar x
        #     ↓
        # validar y
        #     ↓
        # guardar los valores en _x y _y

        if not isinstance(x, (int, float)):
            raise TypeError("x debe ser numérico")

        if not isinstance(y, (int, float)):
            raise TypeError("y debe ser numérico")

        # Los valores se guardan solamente después de superar las
        # validaciones.
        #
        # Usamos un solo guion bajo (_x y _y) porque Python utiliza esta
        # convención para indicar que son atributos internos de la clase.
        #
        # Técnicamente se podría acceder a p._x desde afuera, pero hacerlo
        # significa romper el contrato de la clase.
        #
        # No usamos __x ni __y porque el doble guion bajo activa el
        # mecanismo de name mangling. Se utiliza principalmente para
        # evitar colisiones de nombres en situaciones de herencia.
        self._x = x
        self._y = y

    @property
    def x(self):
        # La property x permite consultar el atributo interno _x.
        #
        # Como no existe @x.setter, x es de solo lectura.
        return self._x

    @property
    def y(self):
        # La property y permite consultar el atributo interno _y.
        #
        # Como no existe @y.setter, y también es de solo lectura.
        return self._y

    def __str__(self):
        return f"({self._x}, {self._y})"


# Creamos un punto válido.
#
# Punto(3, 5)
#     ↓
# se ejecuta __init__()
#     ↓
# x es numérico
#     ↓
# y es numérico
#     ↓
# self._x = 3
# self._y = 5
p = Punto(3, 5)

print(p.x, p.y)  # 3 5
print(p)  # (3, 5)


# Al consultar p.x no accedemos directamente a _x.
#
# p.x
#     ↓
# se ejecuta la property x
#     ↓
# return self._x
print(p.x)  # 3


# Intentamos modificar x mediante la interfaz pública.
#
# p.x = 10
#     ↓
# Python encuentra la property x
#     ↓
# busca un @x.setter
#     ↓
# no existe
#     ↓
# AttributeError
#
# Capturamos la excepción para mostrar el error sin detener el programa.
try:
    p.x = 10
except AttributeError as error:
    print(f"Error: {error}")


# El objeto original no fue modificado.
print(p)  # (3, 5)


# Como x e y son properties de solo lectura, la forma prevista de tener
# otras coordenadas es crear un nuevo objeto.
otro_punto = Punto(10, 5)

print(otro_punto)  # (10, 5)


# También podemos comprobar que la validación ocurre al crear el objeto.
#
# En este caso x no es numérico, por lo que __init__ lanza TypeError.
try:
    punto_invalido = Punto("tres", 5)
except TypeError as error:
    print(f"Error: {error}")
