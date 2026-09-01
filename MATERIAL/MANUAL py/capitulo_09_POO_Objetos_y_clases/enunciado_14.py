# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 14
# Definí una clase Empleado con atributos nombre, sueldo_basico y
# antiguedad_anios. Agregale un método sueldo_total() que devuelva el
# sueldo básico más un 5% por año de antigüedad.
# -------------------------------------------------------------------------


class Empleado:

    def __init__(self, nombre, sueldo_basico, antiguedad_anios):
        self.nombre = nombre
        self.sueldo_basico = sueldo_basico
        self.antiguedad_anios = antiguedad_anios

    def sueldo_total(self):
        aumento = self.sueldo_basico * 0.05 * self.antiguedad_anios
        return self.sueldo_basico + aumento


juan = Empleado("Juan Pérez", 50000, 3)

print(f"${juan.sueldo_total():.2f}")
