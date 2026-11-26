# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ISP: una interfaz MaquinaMultifuncion obliga a implementar imprimir(),
# escanear() y enviar_fax(). ImpresoraSimple solo puede imprimir, así
# que lanza NotImplementedError en los otros dos. Partí la interfaz en
# interfaces chicas para que cada clase implemente solo lo que cumple.
# -------------------------------------------------------------------------

from abc import ABC, abstractmethod


class Impresora(ABC):
    """Interfaz mínima: el equipo sabe imprimir."""

    @abstractmethod
    def imprimir(self, documento):
        """Imprime el documento en papel."""


class Escaner(ABC):
    """Interfaz mínima: el equipo sabe escanear."""

    @abstractmethod
    def escanear(self, documento):
        """Digitaliza el documento."""


class Fax(ABC):
    """Interfaz mínima: el equipo sabe enviar faxes."""

    @abstractmethod
    def enviar_fax(self, documento):
        """Envía el documento por fax."""


class ImpresoraSimple(Impresora):
    """Solo implementa lo que realmente puede hacer."""

    def imprimir(self, documento):
        print(f"Imprimiendo {documento}")


class MultifuncionVieja(Impresora, Escaner, Fax):
    """Equipo completo: cumple las tres interfaces."""

    def imprimir(self, documento):
        print(f"Imprimiendo {documento}")

    def escanear(self, documento):
        print(f"Escaneando {documento}")

    def enviar_fax(self, documento):
        print(f"Enviando por fax {documento}")


def imprimir_todo(equipos, documento):
    """Solo pide imprimir(): no le importa qué más sabe el equipo."""
    for equipo in equipos:
        equipo.imprimir(documento)


if __name__ == "__main__":
    # MultifuncionVieja hereda de tres clases a la vez. Es la única
    # herencia múltiple que usa el manual: las tres bases son ABCs
    # puras, sin estado, o sea interfaces. No hay implementación que
    # resolver, así que no hay problema del diamante.
    imprimir_todo(
        [ImpresoraSimple(), MultifuncionVieja()],
        "informe.pdf",
    )

    MultifuncionVieja().escanear("recibo.pdf")

    # Nadie obliga a la impresora simple a fingir que escanea.
    print(hasattr(ImpresoraSimple(), "escanear"))
