# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Definí una clase Persona con nombre y edad. Hacé Estudiante(Persona)
# que agrega carrera. Sobrescribí __str__ para que la persona imprima
# "Nombre (Edad años)" y el estudiante "Nombre (Edad años, Carrera)".
# Acá la hija reemplaza el formato completo del padre.
# -------------------------------------------------------------------------

class Persona:
    """Persona con nombre y edad."""

    def __init__(self, nombre, edad):
        self._nombre = nombre
        self._edad = edad

    def __str__(self):
        return f"{self._nombre} ({self._edad} años)"


class Estudiante(Persona):
    """Persona que agrega una carrera."""

    def __init__(self, nombre, edad, carrera):
        super().__init__(nombre, edad)
        self._carrera = carrera

    def __str__(self):
        return (
            f"{self._nombre} ({self._edad} años, {self._carrera})"
        )


persona = Persona("Juan", 40)
estudiante = Estudiante("Ana", 22, "Ingeniería")

print(persona)
print(estudiante)
