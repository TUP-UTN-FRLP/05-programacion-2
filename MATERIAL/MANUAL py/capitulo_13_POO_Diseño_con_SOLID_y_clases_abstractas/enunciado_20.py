# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Integrador final: la iteración 5 del banco. Movimiento pasa a ser una
# dataclass frozen; Cuenta se vuelve abstracta con ABC y define el
# esqueleto de extraer(), delegando en puede_extraer(); aparecen
# CuentaAhorro, CuentaCorriente y la nueva CuentaSueldo; Banco deja de
# guardar el dict y recibe un RepositorioCuentas inyectado. Todo con
# type hints. Cerrá verificando con assert que las tres cuentas cumplen
# el contrato del padre.
#
# En el proyecto real cada bloque va en su módulo: errores.py,
# movimientos.py, cuentas.py, repositorios.py, banco.py y main.py.
# -------------------------------------------------------------------------

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Optional

# --- errores.py ------------------------------------------------


class MontoInvalidoError(Exception):
    """Indica que el monto de la operación no es válido."""


class SaldoInsuficienteError(Exception):
    """Indica que la cuenta no tiene fondos para la operación."""


class CuentaNoEncontrada(Exception):
    """Indica que no existe la cuenta solicitada."""


class NumeroDuplicadoError(Exception):
    """Indica que el número de cuenta ya está usado."""


# --- movimientos.py --------------------------------------------


@dataclass(frozen=True)
class Movimiento:
    """Registro inmutable de una operación sobre una cuenta."""

    tipo: str
    monto: float
    saldo_resultante: float

    def __str__(self) -> str:
        return (
            f"{self.tipo:<12} ${self.monto:>10,.2f} "
            f"-> ${self.saldo_resultante:,.2f}"
        )


# --- cuentas.py ------------------------------------------------


class Cuenta(ABC):
    """Cuenta abstracta: define el esqueleto de las operaciones."""

    def __init__(
        self,
        numero: str,
        titular: str,
        saldo: float = 0,
    ) -> None:
        self._numero = numero
        self._titular = titular
        self._saldo = saldo
        self._movimientos: list[Movimiento] = []

    @property
    def numero(self) -> str:
        """Número identificador de la cuenta."""
        return self._numero

    @property
    def saldo(self) -> float:
        """Saldo actual, de solo lectura."""
        return self._saldo

    @abstractmethod
    def puede_extraer(self, monto: float) -> bool:
        """Regla propia de cada tipo de cuenta."""

    @abstractmethod
    def costo_mantenimiento(self) -> float:
        """Costo mensual que cobra el banco por la cuenta."""

    def depositar(self, monto: float) -> None:
        """Acredita un monto positivo y lo registra."""
        if monto <= 0:
            raise MontoInvalidoError("El monto debe ser positivo")

        self._saldo += monto
        self._registrar("depósito", monto)

    def extraer(self, monto: float) -> None:
        """Debita el monto si la regla de la cuenta lo permite."""
        if monto <= 0:
            raise MontoInvalidoError("El monto debe ser positivo")

        if not self.puede_extraer(monto):
            raise SaldoInsuficienteError(
                f"Extracción rechazada en {self._numero}"
            )

        self._saldo -= monto
        self._registrar("extracción", monto)

    def _registrar(self, tipo: str, monto: float) -> None:
        """Agrega un movimiento al historial."""
        self._movimientos.append(
            Movimiento(tipo, monto, self._saldo)
        )

    def historial(self) -> list[Movimiento]:
        """Devuelve una copia del historial de movimientos."""
        return list(self._movimientos)

    def __str__(self) -> str:
        return (
            f"[{self._numero}] {type(self).__name__} de "
            f"{self._titular}: ${self._saldo:,.2f}"
        )


class CuentaAhorro(Cuenta):
    """No admite descubierto y paga mantenimiento."""

    def puede_extraer(self, monto: float) -> bool:
        return monto <= self._saldo

    def costo_mantenimiento(self) -> float:
        return 500


class CuentaCorriente(Cuenta):
    """Admite girar en descubierto hasta un límite."""

    def __init__(
        self,
        numero: str,
        titular: str,
        saldo: float = 0,
        descubierto: float = 50000,
    ) -> None:
        super().__init__(numero, titular, saldo)
        self._descubierto = descubierto

    def puede_extraer(self, monto: float) -> bool:
        return monto <= self._saldo + self._descubierto

    def costo_mantenimiento(self) -> float:
        return 1500


class CuentaSueldo(Cuenta):
    """Tipo nuevo de la iteración 5: sin descubierto ni costo."""

    def puede_extraer(self, monto: float) -> bool:
        return monto <= self._saldo

    def costo_mantenimiento(self) -> float:
        return 0


# --- repositorios.py -------------------------------------------


class RepositorioCuentas(ABC):
    """Abstracción: algo que sabe guardar y recuperar cuentas."""

    @abstractmethod
    def guardar(self, cuenta: Cuenta) -> None:
        """Persiste la cuenta."""

    @abstractmethod
    def obtener(self, numero: str) -> Optional[Cuenta]:
        """Devuelve la cuenta o None si no está."""

    @abstractmethod
    def todas(self) -> list[Cuenta]:
        """Devuelve todas las cuentas guardadas."""


@dataclass
class RepositorioMemoria(RepositorioCuentas):
    """Implementación en memoria, la que usamos por ahora."""

    _cuentas: dict[str, Cuenta] = field(default_factory=dict)

    def guardar(self, cuenta: Cuenta) -> None:
        self._cuentas[cuenta.numero] = cuenta

    def obtener(self, numero: str) -> Optional[Cuenta]:
        return self._cuentas.get(numero)

    def todas(self) -> list[Cuenta]:
        return list(self._cuentas.values())


# --- banco.py --------------------------------------------------


class Banco:
    """ABM de cuentas. No sabe dónde ni cómo se guardan."""

    def __init__(
        self,
        nombre: str,
        repositorio: RepositorioCuentas,
    ) -> None:
        self._nombre = nombre
        self._repositorio = repositorio

    def abrir_cuenta(self, cuenta: Cuenta) -> Cuenta:
        """Registra una cuenta ya construida."""
        if self._repositorio.obtener(cuenta.numero) is not None:
            raise NumeroDuplicadoError(
                f"La cuenta {cuenta.numero} ya existe"
            )

        self._repositorio.guardar(cuenta)

        return cuenta

    def buscar(self, numero: str) -> Cuenta:
        """Devuelve la cuenta pedida o lanza excepción."""
        cuenta = self._repositorio.obtener(numero)

        if cuenta is None:
            raise CuentaNoEncontrada(f"No existe la cuenta {numero}")

        return cuenta

    def listar(self) -> list[Cuenta]:
        """Devuelve todas las cuentas del banco."""
        return self._repositorio.todas()

    def total_depositado(self) -> float:
        """Suma los saldos de todas las cuentas."""
        return sum(cuenta.saldo for cuenta in self.listar())


# --- main.py ---------------------------------------------------


def verificar_contrato(cuentas: list[Cuenta]) -> None:
    """Comprueba que toda subclase de Cuenta cumple lo prometido."""
    for cuenta in cuentas:
        previo = cuenta.saldo
        cuenta.depositar(100)

        assert cuenta.saldo == previo + 100, (
            f"{type(cuenta).__name__} no acreditó el depósito"
        )
        assert cuenta.historial(), (
            f"{type(cuenta).__name__} no registró el movimiento"
        )

    print("Las tres cuentas respetan el contrato de Cuenta")


if __name__ == "__main__":
    banco = Banco("Banco de La Plata", RepositorioMemoria())

    ahorro = banco.abrir_cuenta(CuentaAhorro("A-1", "Ana", 10000))
    corriente = banco.abrir_cuenta(
        CuentaCorriente("C-1", "Juan", 5000)
    )
    sueldo = banco.abrir_cuenta(CuentaSueldo("S-1", "Pedro", 2000))

    ahorro.extraer(4000)
    corriente.extraer(20000)

    for cuenta in banco.listar():
        print(cuenta)

    print(f"Total depositado: ${banco.total_depositado():,.2f}")

    print(f"Historial de {ahorro.numero}:")
    for movimiento in ahorro.historial():
        print(f"  {movimiento}")

    try:
        sueldo.extraer(999999)
    except SaldoInsuficienteError as error:
        print(f"Error: {error}")

    verificar_contrato([ahorro, corriente, sueldo])
