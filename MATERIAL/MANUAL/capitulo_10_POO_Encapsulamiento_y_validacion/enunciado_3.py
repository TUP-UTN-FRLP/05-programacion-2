# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Termometro con _temperatura privada. El setter debe
# rechazar temperaturas menores a −273.15 (cero absoluto en Celsius).
# Lanzá ValueError.
# -------------------------------------------------------------------------


class Termometro:
    def __init__(self, temperatura):
        self.temperatura = temperatura

    @property
    def temperatura(self):
        return self._temperatura

    @temperatura.setter
    def temperatura(self, valor):
        if valor < -273.15:
            raise ValueError("Temperatura menor al cero absoluto")

        self._temperatura = valor


t = Termometro(25)

t.temperatura = -300  # ValueError
