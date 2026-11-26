# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 08
# Sumale a Persona un método es_mayor() que devuelva True si tiene
# 18 o más.
# -------------------------------------------------------------------------


class Persona:

    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def cumplir_años(self):
        self.edad += 1

    def es_mayor(self):
        return self.edad >= 18


ana = Persona("Ana", 25)
juan = Persona("Juanito", 15)

print(f"{ana.nombre} es mayor: {ana.es_mayor()}")
print(f"{juan.nombre} es mayor: {juan.es_mayor()}")
