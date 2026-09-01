# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 16
# Definí una clase Termometro con atributo temperatura (en Celsius).
# Agregale métodos a_fahrenheit() y a_kelvin() que devuelvan la
# temperatura en esas escalas.
# -------------------------------------------------------------------------


class Termometro:

    def __init__(self, temperatura):
        self.temperatura = temperatura

    def a_fahrenheit(self):
        return self.temperatura * 9 / 5 + 32

    def a_kelvin(self):
        return self.temperatura + 273.15


t = Termometro(25)

print(
    f"{t.temperatura}°C = "
    f"{t.a_fahrenheit()}°F = {t.a_kelvin()}K"
)
