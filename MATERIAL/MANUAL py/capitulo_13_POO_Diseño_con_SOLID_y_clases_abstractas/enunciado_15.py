# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# assert como verificación de contrato: escribí verificar_liskov(clases)
# que reciba subclases de Cuenta y compruebe que todas cumplen lo que el
# padre promete: saldo inicial no negativo, depositar(x) aumenta el saldo
# exactamente en x, y saldo es una property de solo lectura. Chequeá la
# property de verdad, no con un acceso que cualquier atributo pasaría.
# -------------------------------------------------------------------------

from abc import ABC, abstractmethod


class Cuenta(ABC):
    """Cuenta abstracta con saldo expuesto como property."""

    def __init__(self, saldo_inicial: float = 0) -> None:
        self._saldo = saldo_inicial

    @property
    def saldo(self) -> float:
        """Saldo actual de la cuenta, de solo lectura."""
        return self._saldo

    @abstractmethod
    def depositar(self, monto: float) -> None:
        """Acredita el monto en la cuenta."""


class CuentaAhorro(Cuenta):
    """Cuenta de ahorro que cumple el contrato."""

    def depositar(self, monto: float) -> None:
        self._saldo += monto


class CuentaCorriente(Cuenta):
    """Cuenta corriente que cumple el contrato."""

    def depositar(self, monto: float) -> None:
        self._saldo += monto


class CuentaTramposa(Cuenta):
    """Rompe el contrato: se queda con una comisión del depósito."""

    def depositar(self, monto: float) -> None:
        self._saldo += monto - 50


def verificar_liskov(clases: list[type]) -> None:
    """Verifica que cada subclase respete el contrato de Cuenta."""
    for clase in clases:
        nombre = clase.__name__
        cuenta = clase(1000)

        assert cuenta.saldo >= 0, f"{nombre}: saldo inicial negativo"

        # Comprobación real de que saldo es una property.
        assert isinstance(getattr(clase, "saldo"), property), (
            f"{nombre}: saldo no es una property"
        )

        previo = cuenta.saldo
        cuenta.depositar(100)
        assert cuenta.saldo == previo + 100, (
            f"{nombre}: depositar(100) no sumó 100 al saldo"
        )

        print(f"  {nombre} cumple el contrato")


if __name__ == "__main__":
    verificar_liskov([CuentaAhorro, CuentaCorriente])

    try:
        verificar_liskov([CuentaTramposa])
    except AssertionError as error:
        print(f"Violación detectada: {error}")
