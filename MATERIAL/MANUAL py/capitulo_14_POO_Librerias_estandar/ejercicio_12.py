# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Cierre: hacé que el banco de los capítulos 12 y 13 sobreviva al
# apagado. Dale a Movimiento y a Cuenta métodos to_dict() y
# from_dict(), guardá todas las cuentas en banco.json y volvé a
# cargarlas en un programa nuevo. Verificá con assert que los saldos y
# los historiales se conservan intactos.
# -------------------------------------------------------------------------

import json
from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True)
class Movimiento:
    """Registro inmutable de una operación sobre una cuenta."""

    tipo: str
    monto: float
    fecha: str

    def to_dict(self):
        """Devuelve el movimiento como diccionario serializable."""
        return asdict(self)

    @classmethod
    def from_dict(cls, datos):
        """Reconstruye un Movimiento desde un diccionario."""
        return cls(**datos)


class Cuenta:
    """Cuenta que sabe convertirse a diccionario y volver."""

    def __init__(self, numero, titular, saldo=0, movimientos=None):
        self._numero = numero
        self._titular = titular
        self._saldo = saldo
        self._movimientos = list(movimientos or [])

    @property
    def numero(self):
        """Número identificador de la cuenta."""
        return self._numero

    @property
    def saldo(self):
        """Saldo actual de la cuenta."""
        return self._saldo

    def depositar(self, monto):
        """Acredita un monto positivo y lo registra."""
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")

        self._saldo += monto
        self._movimientos.append(
            Movimiento(
                "depósito",
                monto,
                datetime.now().isoformat(timespec="seconds"),
            )
        )

    def historial(self):
        """Devuelve una copia del historial de movimientos."""
        return list(self._movimientos)

    def to_dict(self):
        """Devuelve la cuenta como diccionario serializable."""
        return {
            "numero": self._numero,
            "titular": self._titular,
            "saldo": self._saldo,
            "movimientos": [
                movimiento.to_dict()
                for movimiento in self._movimientos
            ],
        }

    @classmethod
    def from_dict(cls, datos):
        """Reconstruye una Cuenta desde un diccionario."""
        return cls(
            numero=datos["numero"],
            titular=datos["titular"],
            saldo=datos["saldo"],
            movimientos=[
                Movimiento.from_dict(movimiento)
                for movimiento in datos["movimientos"]
            ],
        )

    def __str__(self):
        return f"[{self._numero}] {self._titular}: ${self._saldo}"


def guardar_banco(cuentas, ruta):
    """Guarda todas las cuentas del banco en un archivo JSON."""
    ruta.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(
            [cuenta.to_dict() for cuenta in cuentas],
            archivo,
            indent=2,
            ensure_ascii=False,
        )


def cargar_banco(ruta):
    """Reconstruye las cuentas del banco desde un archivo JSON."""
    with open(ruta, encoding="utf-8") as archivo:
        return [Cuenta.from_dict(datos) for datos in json.load(archivo)]


if __name__ == "__main__":
    # to_dict/from_dict es el puente entre nuestros objetos y JSON,
    # que solo entiende tipos básicos. from_dict es un classmethod:
    # un "constructor alternativo" que devuelve una instancia.
    ruta = Path("datos") / "banco.json"

    ahorro = Cuenta("A-1", "Ana Pérez", 10000)
    ahorro.depositar(2500)

    corriente = Cuenta("C-1", "Juan Gómez", 5000)

    guardar_banco([ahorro, corriente], ruta)

    recuperadas = cargar_banco(ruta)

    for cuenta in recuperadas:
        print(cuenta)

    assert recuperadas[0].saldo == ahorro.saldo, "Cambió el saldo"
    assert recuperadas[0].historial() == ahorro.historial(), (
        "Se perdió el historial"
    )

    print("El banco sobrevivió al apagado")
