# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Protocol: declará un protocolo Exportable con un método a_csv() que
# devuelva una línea de texto. Después hacé dos clases sin relación de
# herencia entre sí, Alumno y Materia, que lo cumplan, y una función
# exportar(elementos) tipada con list[Exportable]. Verificá con
# isinstance usando @runtime_checkable.
# -------------------------------------------------------------------------

from typing import Protocol, runtime_checkable


@runtime_checkable
class Exportable(Protocol):
    """Cualquier objeto que sepa representarse como línea CSV."""

    def a_csv(self) -> str:
        """Devuelve los datos del objeto separados por comas."""
        ...


class Alumno:
    """Alumno que cumple el protocolo sin heredar de él."""

    def __init__(self, legajo: str, nombre: str) -> None:
        self._legajo = legajo
        self._nombre = nombre

    def a_csv(self) -> str:
        return f"{self._legajo},{self._nombre}"


class Materia:
    """Materia que también lo cumple, sin ancestro común."""

    def __init__(self, codigo: str, nombre: str) -> None:
        self._codigo = codigo
        self._nombre = nombre

    def a_csv(self) -> str:
        return f"{self._codigo},{self._nombre}"


class Aula:
    """No cumple el protocolo: no tiene a_csv()."""

    def __init__(self, numero: int) -> None:
        self._numero = numero


def exportar(elementos: list[Exportable]) -> str:
    """Arma un CSV con cualquier objeto que sepa exportarse."""
    return "\n".join(elemento.a_csv() for elemento in elementos)


if __name__ == "__main__":
    # Protocol requiere Python 3.8 o superior.
    print(
        exportar(
            [
                Alumno("L-001", "Ana"),
                Materia("PR2", "Programación 2"),
            ]
        )
    )

    # Con @runtime_checkable, isinstance mira la forma, no la herencia.
    print(isinstance(Alumno("L-002", "Juan"), Exportable))
    print(isinstance(Aula(101), Exportable))
