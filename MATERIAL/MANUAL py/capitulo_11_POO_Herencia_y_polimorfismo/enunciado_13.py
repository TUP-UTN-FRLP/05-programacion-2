# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Cuenta con titular y saldo, un método comision() que
# devuelve 50 y un método extraer(monto) que valida que haya saldo
# suficiente, descuenta monto más comision() e informa el resultado.
# Hacé CuentaVIP(Cuenta) que sobrescriba únicamente comision() para
# devolver 0. Fijate que no hace falta reescribir extraer(): el padre
# llama a self.comision() y Python resuelve cuál usar según el objeto.
# -------------------------------------------------------------------------

class Cuenta:
    """Cuenta que cobra una comisión fija en cada extracción."""

    def __init__(self, titular, saldo):
        self._titular = titular
        self._saldo = saldo

    def comision(self):
        """Costo fijo que cobra el banco por extraer."""
        return 50

    def extraer(self, monto):
        """Extrae monto más comisión si el saldo alcanza."""
        if monto <= 0:
            print("El monto debe ser positivo")
            return False
        total = monto + self.comision()
        if total > self._saldo:
            print(f"{self._titular}: saldo insuficiente")
            return False
        self._saldo -= total
        print(
            f"{self._titular}: extrajo ${monto}, "
            f"comisión ${self.comision()}, saldo ${self._saldo}"
        )
        return True


class CuentaVIP(Cuenta):
    """Cuenta que no paga comisión por extraer."""

    def comision(self):
        return 0


cuenta = Cuenta("Ana", 1000)
vip = CuentaVIP("Pedro", 1000)

cuenta.extraer(100)
vip.extraer(100)
cuenta.extraer(5000)
