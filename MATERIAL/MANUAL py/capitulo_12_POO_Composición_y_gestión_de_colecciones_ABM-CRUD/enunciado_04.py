# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Continuando el ejercicio 3, sumale buscar_por_legajo(legajo), que
# devuelva el alumno correspondiente o lance una excepción propia si no
# lo encuentra. Probá los dos caminos: el que encuentra y el que falla.
# -------------------------------------------------------------------------

class AlumnoNoEncontrado(Exception):
    """Indica que no existe un alumno con el legajo solicitado."""

    pass


class Alumno:
    """Alumno identificado por nombre y legajo."""

    def __init__(self, nombre, legajo):
        self._nombre = nombre
        self._legajo = legajo

    def legajo(self):
        """Devuelve el legajo del alumno."""
        return self._legajo

    def __str__(self):
        return f"[{self._legajo}] {self._nombre}"


class Curso:
    """Curso que administra y busca alumnos por legajo."""

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

    def buscar_por_legajo(self, legajo):
        """Devuelve el alumno con ese legajo o lanza excepción."""
        for alumno in self._alumnos:
            if alumno.legajo() == legajo:
                return alumno

        raise AlumnoNoEncontrado(
            f"No hay alumno con legajo {legajo}"
        )


if __name__ == "__main__":
    curso = Curso("Programación 2")
    curso.inscribir(Alumno("Ana", "L-001"))
    curso.inscribir(Alumno("Juan", "L-002"))

    print(curso.buscar_por_legajo("L-001"))

    try:
        curso.buscar_por_legajo("L-999")
    except AlumnoNoEncontrado as error:
        print(f"Error: {error}")
