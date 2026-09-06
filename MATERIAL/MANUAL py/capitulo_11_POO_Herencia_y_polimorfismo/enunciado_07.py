# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Empleado con nombre y método sueldo() que devuelve 0.
# Hacé EmpleadoAsalariado(nombre, sueldo_fijo) y
# EmpleadoComision(nombre, base, ventas, porcentaje). Las dos
# sobrescriben sueldo(). Listá la plantilla y calculá el gasto total
# recorriendo la lista una sola vez, sin preguntar tipos.
# -------------------------------------------------------------------------

class Empleado:
    """Empleado base con sueldo genérico."""

    def __init__(self, nombre):
        self._nombre = nombre

    def sueldo(self):
        """Sueldo por defecto de un empleado sin especializar."""
        return 0

    def __str__(self):
        return f"{self._nombre}: ${self.sueldo():.2f}"


class EmpleadoAsalariado(Empleado):
    """Empleado con sueldo fijo mensual."""

    def __init__(self, nombre, sueldo_fijo):
        super().__init__(nombre)
        self._sueldo_fijo = sueldo_fijo

    def sueldo(self):
        return self._sueldo_fijo


class EmpleadoComision(Empleado):
    """Empleado con sueldo base más comisión sobre ventas."""

    def __init__(self, nombre, base, ventas, porcentaje):
        super().__init__(nombre)
        self._base = base
        self._ventas = ventas
        self._porcentaje = porcentaje

    def sueldo(self):
        comision = self._ventas * self._porcentaje / 100
        return self._base + comision


plantilla = [
    EmpleadoAsalariado("Ana", 500000),
    EmpleadoComision("Juan", 200000, 3000000, 5),
    EmpleadoAsalariado("Pedro", 800000),
]

for empleado in plantilla:
    print(empleado)

total = sum(empleado.sueldo() for empleado in plantilla)
print(f"Gasto total: ${total:.2f}")
