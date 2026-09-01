# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Convertí la clase Punto del capítulo anterior para que x e y sean
# privados y expuestos como properties de solo lectura. El único modo de
# "cambiarlos" es crear un nuevo Punto.
# -------------------------------------------------------------------------


class Punto:
    def __init__(self, x, y):
        # En este caso no existen setters para x e y.
        #
        # La validación se realiza directamente en el constructor antes
        # de guardar los valores.
        #
        # Secuencia para x:
        #
        # x recibido
        #     ↓
        # validación de tipo
        #     ↓
        # si es válido
        #     ↓
        # self._x = x
        #
        # Lo mismo ocurre con y.

        if not isinstance(x, (int, float)):
            raise TypeError("x debe ser numérico")

        if not isinstance(y, (int, float)):
            raise TypeError("y debe ser numérico")

        # Los valores se almacenan recién después de superar las
        # validaciones.
        #
        # Usamos un solo guion bajo (_x y _y) porque en Python indica,
        # por convención, que estos atributos son de uso interno de la
        # clase.
        #
        # Python permite técnicamente acceder a p._x desde afuera, pero
        # hacerlo significa romper el contrato de la clase.
        #
        # No usamos __x o __y porque el doble guion bajo produce name
        # mangling y se reserva principalmente para evitar colisiones
        # de nombres en situaciones de herencia.
        self._x = x
        self._y = y

    @property
    def x(self):
        # x es la interfaz pública para consultar _x.
        #
        # Como no existe @x.setter, la property es de solo lectura.
        return self._x

    @property
    def y(self):
        # y es la interfaz pública para consultar _y.
        #
        # Como no existe @y.setter, tampoco puede modificarse desde la
        # interfaz pública.
        return self._y

    def __str__(self):
        # Devuelve una representación amigable del punto.
        return f"({self._x}, {self._y})"


# Al crear el objeto:
#
# Punto(3, 5)
#     ↓
# __init__()
#     ↓
# valida que x sea int o float
#     ↓
# valida que y sea int o float
#     ↓
# self._x = 3
# self._y = 5
p = Punto(3, 5)

print(p.x, p.y)  # 3 5
print(p)  # (3, 5)


# Cuando escribimos:
#
# p.x
#
# Python ejecuta automáticamente la property:
#
# @property
# def x(self):
#     return self._x
#
# Por eso podemos consultar x como si fuera un atributo normal.
print(p.x)  # 3


# Intentamos modificar x mediante la interfaz pública:
#
# p.x = 10
#     ↓
# Python busca @x.setter
#     ↓
# no existe
#     ↓
# AttributeError
#
# Usamos try/except para mostrar el error sin detener el programa con
# todo el traceback.
try:
    p.x = 10
except AttributeError as error:
    print(f"Error: {error}")


# El punto original continúa teniendo los mismos valores.
print(p)  # (3, 5)


# Como x e y son de solo lectura, la forma prevista de obtener otras
# coordenadas es crear otro objeto Punto.
otro_punto = Punto(10, 5)

print(otro_punto)  # (10, 5)
