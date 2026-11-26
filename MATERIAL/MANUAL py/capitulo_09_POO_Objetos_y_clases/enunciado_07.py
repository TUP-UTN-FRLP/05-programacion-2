# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 07
# Definí una clase Persona con atributos nombre y edad. Agregale un
# método cumplir_años() que suma 1 a la edad.
# -------------------------------------------------------------------------


class Persona:

    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def cumplir_años(self):
        self.edad += 1


ana = Persona("Ana", 25)

print(ana.edad)

ana.cumplir_años()

print(ana.edad)

ana.cumplir_años()

print(ana.edad)
