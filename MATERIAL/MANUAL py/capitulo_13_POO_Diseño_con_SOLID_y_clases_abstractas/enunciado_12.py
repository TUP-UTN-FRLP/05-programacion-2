# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ISP: te dan una clase base Trabajador que obliga a implementar
# trabajar(), comer(), dormir() y cobrar_sueldo(). Robot hereda de ella
# y en tres de los cuatro métodos lanza NotImplementedError. Partí esa
# interfaz gigante en interfaces chicas y hacé que cada clase implemente
# solo lo que puede cumplir.
# -------------------------------------------------------------------------

from abc import ABC, abstractmethod


class SabeTrabajar(ABC):
    """Interfaz mínima: el objeto puede realizar tareas."""

    @abstractmethod
    def trabajar(self) -> None:
        """Ejecuta la tarea asignada."""


class NecesitaDescanso(ABC):
    """Interfaz mínima: el ser come y duerme."""

    @abstractmethod
    def comer(self) -> None:
        """Se alimenta."""

    @abstractmethod
    def dormir(self) -> None:
        """Descansa."""


class RecibeRemuneracion(ABC):
    """Interfaz mínima: el objeto cobra por su trabajo."""

    @abstractmethod
    def cobrar_sueldo(self) -> None:
        """Percibe su remuneración."""


class Humano(SabeTrabajar, NecesitaDescanso, RecibeRemuneracion):
    """Implementa las tres interfaces porque cumple las tres."""

    def trabajar(self) -> None:
        print("Trabajando")

    def comer(self) -> None:
        print("Comiendo")

    def dormir(self) -> None:
        print("Durmiendo")

    def cobrar_sueldo(self) -> None:
        print("Cobrando el sueldo")


class Robot(SabeTrabajar):
    """Implementa solo la interfaz que puede cumplir."""

    def trabajar(self) -> None:
        print("Ejecutando tarea")


def poner_a_trabajar(equipo: list[SabeTrabajar]) -> None:
    """Solo pide trabajar(): no le importa nada más del objeto."""
    for integrante in equipo:
        integrante.trabajar()


if __name__ == "__main__":
    # Humano hereda de tres clases a la vez. Es la única forma de
    # herencia múltiple que usa este manual: las tres bases son ABCs
    # puras, sin estado ni __init__ propio, o sea interfaces. No hay
    # problema del diamante porque no hay implementación que resolver.
    poner_a_trabajar([Humano(), Robot()])

    Humano().cobrar_sueldo()

    # El robot no cobra sueldo y nadie lo obliga a fingir que sí.
    print(hasattr(Robot(), "cobrar_sueldo"))
