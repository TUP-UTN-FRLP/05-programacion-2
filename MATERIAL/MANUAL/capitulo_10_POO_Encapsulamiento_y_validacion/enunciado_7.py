# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Empleado con _sueldo_basico privado y expuesto como
# property. El setter debe rechazar sueldos negativos. Sumale un método
# aumentar_sueldo(porcentaje) que valide que el porcentaje sea positivo.
# -------------------------------------------------------------------------


class Empleado:
    def __init__(self, nombre, sueldo_basico):
        self._nombre = nombre
        self.sueldo_basico = sueldo_basico

    @property
    def sueldo_basico(self):
        return self._sueldo_basico

    @sueldo_basico.setter
    def sueldo_basico(self, valor):
        if valor < 0:
            raise ValueError("El sueldo no puede ser negativo")

        self._sueldo_basico = valor

    def aumentar_sueldo(self, porcentaje):
        if porcentaje <= 0:
            raise ValueError("El porcentaje debe ser positivo")

        self._sueldo_basico *= 1 + porcentaje / 100


e = Empleado("Ana", 50000)

e.aumentar_sueldo(10)

print(e.sueldo_basico)  # 55000.0
