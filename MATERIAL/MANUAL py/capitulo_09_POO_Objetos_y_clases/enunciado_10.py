# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 10
# Sumale a Auto un método mostrar_estado() que imprima "Ford Focus
# circulando a 40 km/h".
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

    def mostrar_estado(self):
        print(
            f"{self.marca} {self.modelo} "
            f"circulando a {self.velocidad_actual} km/h"
        )


focus = Auto("Ford", "Focus")

focus.acelerar()
focus.acelerar()
focus.acelerar()

focus.mostrar_estado()
