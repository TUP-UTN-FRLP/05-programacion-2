# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Continuando el ejercicio 2, hacé Profesor(Persona) que agrega materia
# y antiguedad. Sobrescribí __str__. Después creá una lista con dos
# estudiantes y dos profesores. Recorré e imprimí cada uno: el bucle es
# el mismo para todos y cada objeto imprime su propio formato.
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


class Profesor(Persona):
    """Persona que agrega materia y antigüedad docente."""

    def __init__(self, nombre, edad, materia, antiguedad):
        super().__init__(nombre, edad)
        self._materia = materia
        self._antiguedad = antiguedad

    def __str__(self):
        return (
            f"{self._nombre} ({self._edad} años, "
            f"enseña {self._materia}, "
            f"{self._antiguedad} años de antigüedad)"
        )


gente = [
    Estudiante("Ana", 22, "Ingeniería"),
    Estudiante("Pedro", 20, "Matemática"),
    Profesor("Juan", 45, "Programación 2", 10),
    Profesor("Lucía", 50, "Investigación Operativa", 15),
]

for persona in gente:
    print(persona)
