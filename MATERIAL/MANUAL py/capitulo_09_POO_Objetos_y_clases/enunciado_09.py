# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 09
# Definí una clase Auto con atributos marca, modelo y velocidad_actual
# (que arranca en 0). Agregale métodos acelerar() (suma 10) y frenar()
# (resta 10, pero nunca por debajo de 0).
# -------------------------------------------------------------------------


class Auto:

    def __init__(self, marca, modelo):
        self.marca = marca
        self.modelo = modelo
        self.velocidad_actual = 0

    def acelerar(self):
        self.velocidad_actual += 10

    def frenar(self):
        self.velocidad_actual -= 10

        if self.velocidad_actual < 0:
            self.velocidad_actual = 0


focus = Auto("Ford", "Focus")

focus.acelerar()
focus.acelerar()
focus.acelerar()

print(focus.velocidad_actual)

focus.frenar()

print(focus.velocidad_actual)

focus.frenar()
focus.frenar()
focus.frenar()

print(focus.velocidad_actual)
