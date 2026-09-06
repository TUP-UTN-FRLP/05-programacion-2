# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Modelá una clase Curso que tiene un nombre y una lista de Alumno.
# Cada Alumno tiene nombre y legajo. Agregá los métodos
# inscribir(alumno), cantidad_inscriptos() y listar_alumnos(). El
# nombre del curso se muestra con __str__, no leyendo el atributo
# desde afuera.
# -------------------------------------------------------------------------

class Alumno:
    """Alumno identificado por nombre y legajo."""

    def __init__(self, nombre, legajo):
        self._nombre = nombre
        self._legajo = legajo

    def __str__(self):
        return f"[{self._legajo}] {self._nombre}"


class Curso:
    """Curso que contiene una colección de alumnos."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._alumnos = []

    def inscribir(self, alumno):
        """Agrega un alumno a la lista de inscriptos."""
        self._alumnos.append(alumno)

    def cantidad_inscriptos(self):
        """Devuelve cuántos alumnos hay inscriptos."""
        return len(self._alumnos)

    def listar_alumnos(self):
        """Imprime todos los alumnos inscriptos."""
        for alumno in self._alumnos:
            print(f"  {alumno}")

    def __str__(self):
        return (
            f"Inscriptos en {self._nombre}: "
            f"{self.cantidad_inscriptos()}"
        )


if __name__ == "__main__":
    curso = Curso("Programación 2")
    curso.inscribir(Alumno("Ana", "L-001"))
    curso.inscribir(Alumno("Juan", "L-002"))
    curso.inscribir(Alumno("Pedro", "L-003"))

    print(curso)
    curso.listar_alumnos()
