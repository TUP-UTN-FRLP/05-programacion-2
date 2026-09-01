# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Ampliá la clase Rectangulo para que base y altura sean properties con
# setters que rechacen valores no positivos.
# -------------------------------------------------------------------------


class Rectangulo:
    def __init__(self, base, altura):
        # No guardamos directamente en self._base y self._altura.
        #
        # Al escribir self.base y self.altura se ejecutan los setters.
        # De esta manera, los valores se validan también cuando se crea
        # el objeto.
        #
        # Secuencia:
        # self.base = base
        #       ↓
        # setter de base
        #       ↓
        # validación
        #       ↓
        # self._base = valor
        self.base = base
        self.altura = altura

    @property
    def base(self):
        # base es la propiedad pública.
        # _base es el atributo interno donde se guarda el valor.
        return self._base

    @base.setter
    def base(self, valor):
        # Este método se ejecuta automáticamente cuando hacemos:
        # objeto.base = valor
        if valor <= 0:
            raise ValueError("La base debe ser positiva")

        # El valor se guarda recién después de superar la validación.
        #
        # Usamos un solo guion bajo porque en Python indica, por
        # convención, que el atributo es de uso interno de la clase.
        # No impide técnicamente el acceso desde afuera, pero comunica
        # que no debería modificarse directamente.
        #
        # No usamos __base porque el doble guion bajo produce name
        # mangling y se reserva principalmente para evitar colisiones
        # de nombres en situaciones de herencia.
        self._base = valor

    @property
    def altura(self):
        # altura es la propiedad pública.
        # _altura contiene internamente el valor.
        return self._altura

    @altura.setter
    def altura(self, valor):
        # Este setter se ejecuta automáticamente cuando hacemos:
        # objeto.altura = valor
        if valor <= 0:
            raise ValueError("La altura debe ser positiva")

        # Solo almacenamos el valor si pasó la validación.
        self._altura = valor

    @property
    def area(self):
        # area es una property de solo lectura porque no tiene setter.
        # No necesita guardarse: se calcula cada vez que se consulta.
        return self._base * self._altura


# Al crear el objeto:
#
# Rectangulo(5, 3)
#       ↓
# __init__()
#       ↓
# self.base = 5   → setter de base   → valida → self._base = 5
# self.altura = 3 → setter de altura → valida → self._altura = 3
r = Rectangulo(5, 3)

print(r.area)  # 15


# La asignación no modifica _base directamente.
# Primero se ejecuta el setter de base:
#
# r.base = 10
#       ↓
# setter de base
#       ↓
# 10 > 0
#       ↓
# self._base = 10
r.base = 10

print(r.area)  # 30


# Intentamos asignar una altura inválida.
#
# r.altura = -1
#       ↓
# setter de altura
#       ↓
# -1 <= 0
#       ↓
# raise ValueError
#
# Usamos try/except para mostrar el error sin detener el programa con
# todo el traceback.
try:
    r.altura = -1
except ValueError as error:
    print(f"Error: {error}")
