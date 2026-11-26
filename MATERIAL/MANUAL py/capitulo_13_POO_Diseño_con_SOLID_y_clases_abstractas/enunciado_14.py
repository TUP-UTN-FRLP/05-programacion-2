# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Protocol: escribí filtrar(elementos, criterio) tipada con
# Callable[[T], bool], y una función informar(cosas) que acepte
# cualquier objeto con un método describir(), declarado como Protocol.
# Fijate que las clases que lo cumplen no heredan de nada: el Protocol
# describe la forma, no la ascendencia.
# -------------------------------------------------------------------------

from typing import Callable, Protocol, TypeVar

T = TypeVar("T")


class Describible(Protocol):
    """Cualquier objeto que sepa describirse en una línea."""

    def describir(self) -> str:
        """Devuelve una descripción legible del objeto."""
        ...


class Alumno:
    """Alumno con nombre y promedio. No hereda de Describible."""

    def __init__(self, nombre: str, promedio: float) -> None:
        self._nombre = nombre
        self._promedio = promedio

    def promedio(self) -> float:
        """Devuelve el promedio del alumno."""
        return self._promedio

    def describir(self) -> str:
        return f"Alumno {self._nombre} ({self._promedio})"


class Materia:
    """Materia con nombre y año. Tampoco hereda de nada."""

    def __init__(self, nombre: str, anio: int) -> None:
        self._nombre = nombre
        self._anio = anio

    def describir(self) -> str:
        return f"Materia {self._nombre} ({self._anio}º año)"


def filtrar(
    elementos: list[T],
    criterio: Callable[[T], bool],
) -> list[T]:
    """Devuelve los elementos que cumplen el criterio."""
    return [
        elemento
        for elemento in elementos
        if criterio(elemento)
    ]


def informar(cosas: list[Describible]) -> None:
    """Describe cualquier objeto que tenga describir()."""
    for cosa in cosas:
        print(f"  {cosa.describir()}")


if __name__ == "__main__":
    # Protocol requiere Python 3.8 o superior.
    alumnos = [
        Alumno("Ana", 8.5),
        Alumno("Juan", 5.0),
        Alumno("Pedro", 9.2),
    ]

    aprobados = filtrar(alumnos, lambda a: a.promedio() >= 6)
    informar(aprobados)

    # Alumno y Materia no comparten ancestro, pero las dos cumplen el
    # protocolo: alcanza con tener describir().
    informar([Alumno("Lucía", 7.0), Materia("Programación 2", 2)])
