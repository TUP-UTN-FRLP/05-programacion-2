# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 15
# Sumale a Empleado un __str__ que muestre "Juan Pérez, Antigüedad:
# 3 años, Sueldo total: $52500.00".
# -------------------------------------------------------------------------


class Empleado:

    def __init__(self, nombre, sueldo_basico, antiguedad_anios):
        self.nombre = nombre
        self.sueldo_basico = sueldo_basico
        self.antiguedad_anios = antiguedad_anios

    def sueldo_total(self):
        aumento = (
            self.sueldo_basico * 0.05 * self.antiguedad_anios
        )
        return self.sueldo_basico + aumento

    def __str__(self):
        return (
            f"{self.nombre} - "
            f"Antigüedad: {self.antiguedad_anios} años - "
            f"Sueldo total: ${self.sueldo_total():.2f}"
        )


juan = Empleado("Juan Pérez", 50000, 3)

print(juan)
