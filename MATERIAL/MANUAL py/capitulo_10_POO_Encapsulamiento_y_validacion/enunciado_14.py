# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Circulo con _radio privado (positivo). Properties de
# solo lectura: area, perimetro, diametro. Un setter para radio que
# valide.
# -------------------------------------------------------------------------

import math


class Circulo:
    def __init__(self, radio):
        # No guardamos directamente:
        # self._radio = radio
        #
        # Usamos la property:
        # self.radio = radio
        #
        # De esta forma el setter también valida el radio cuando se
        # crea el objeto.
        #
        # Secuencia:
        # Circulo(radio)
        #       ↓
        # __init__()
        #       ↓
        # self.radio = radio
        #       ↓
        # setter de radio
        #       ↓
        # validar que sea positivo
        #       ↓
        # self._radio = valor
        self.radio = radio

    @property
    def radio(self):
        # radio es la property pública.
        # _radio es el atributo interno donde se guarda el valor.
        return self._radio

    @radio.setter
    def radio(self, valor):
        # Este setter se ejecuta cuando hacemos:
        # circulo.radio = valor
        #
        # El radio debe ser mayor que cero.
        if valor <= 0:
            raise ValueError("El radio debe ser positivo")

        # El valor se guarda solamente después de superar la validación.
        #
        # Usamos un solo guion bajo (_radio) porque en Python indica,
        # por convención, que el atributo es de uso interno de la clase.
        # Técnicamente puede accederse desde afuera, pero hacerlo
        # significa romper el contrato de la clase.
        #
        # No usamos __radio porque el doble guion bajo activa name
        # mangling, usado principalmente para evitar colisiones de
        # nombres en situaciones de herencia.
        self._radio = valor

    @property
    def area(self):
        # area es una property de solo lectura porque no tiene setter.
        # No guardamos un atributo _area: el valor se calcula cada vez
        # que se consulta.
        return math.pi * self._radio ** 2

    @property
    def perimetro(self):
        # perimetro también es una property calculada de solo lectura.
        return 2 * math.pi * self._radio

    @property
    def diametro(self):
        # diametro también se calcula a partir del radio actual.
        return 2 * self._radio


# ---------------------------------------------------------------
# CASO 1: creación de un círculo válido
#
# Circulo(5)
#       ↓
# __init__()
#       ↓
# self.radio = 5
#       ↓
# setter
#       ↓
# 5 > 0
#       ↓
# self._radio = 5
# ---------------------------------------------------------------

circulo = Circulo(5)

print(f"Radio: {circulo.radio:.2f}")
print(f"Área: {circulo.area:.2f}")
print(f"Perímetro: {circulo.perimetro:.2f}")
print(f"Diámetro: {circulo.diametro:.2f}")


# ---------------------------------------------------------------
# CASO 2: modificar el radio
#
# circulo.radio = 10
#       ↓
# setter
#       ↓
# 10 > 0
#       ↓
# self._radio = 10
#
# area, perimetro y diametro no necesitan actualizarse manualmente.
# Se calculan nuevamente cuando se consultan.
# ---------------------------------------------------------------

circulo.radio = 10

print(f"Radio: {circulo.radio:.2f}")
print(f"Área: {circulo.area:.2f}")
print(f"Perímetro: {circulo.perimetro:.2f}")
print(f"Diámetro: {circulo.diametro:.2f}")


# ---------------------------------------------------------------
# CASO 3: intento de asignar un radio inválido
#
# circulo.radio = -3
#       ↓
# setter
#       ↓
# -3 <= 0
#       ↓
# ValueError
# ---------------------------------------------------------------

try:
    circulo.radio = -3
except ValueError as error:
    print(f"Error: {error}")


# El valor inválido fue rechazado y el radio anterior se conserva.
print(f"Radio actual: {circulo.radio:.2f}")


# ---------------------------------------------------------------
# CASO 4: creación de un círculo con radio inválido
#
# Como __init__ utiliza la property, el setter también protege la
# creación del objeto.
# ---------------------------------------------------------------

try:
    circulo_invalido = Circulo(0)
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 5: intento de modificar una property de solo lectura
#
# area tiene @property pero no tiene @area.setter.
# Por eso no puede asignarse directamente.
#
# circulo.area = 100
#       ↓
# Python busca @area.setter
#       ↓
# no existe
#       ↓
# AttributeError
# ---------------------------------------------------------------

try:
    circulo.area = 100
except AttributeError as error:
    print(f"Error: {error}")
