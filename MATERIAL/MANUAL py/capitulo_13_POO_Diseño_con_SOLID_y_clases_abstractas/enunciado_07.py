# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# LSP: analizá esta jerarquía. Cuenta.extraer() extrae si hay saldo y
# lanza SaldoInsuficienteError si no alcanza. CuentaBloqueada(Cuenta)
# sobrescribe extraer() y siempre lanza PermissionError, incluso con
# saldo de sobra. ¿Viola el principio? Justificá y proponé un modelo
# mejor.
# -------------------------------------------------------------------------

class SaldoInsuficienteError(Exception):
    """Indica que la cuenta no tiene fondos suficientes."""

    pass


class CuentaBloqueadaError(Exception):
    """Indica que la cuenta está bloqueada operativamente."""

    pass


class Cuenta:
    """Cuenta cuyo bloqueo es un estado, no un subtipo."""

    def __init__(self, numero, saldo=0):
        self._numero = numero
        self._saldo = saldo
        self._bloqueada = False

    def saldo(self):
        """Devuelve el saldo actual."""
        return self._saldo

    def esta_bloqueada(self):
        """Informa si la cuenta está bloqueada."""
        return self._bloqueada

    def bloquear(self):
        """Impide operar con la cuenta hasta desbloquearla."""
        self._bloqueada = True

    def desbloquear(self):
        """Vuelve a habilitar las operaciones."""
        self._bloqueada = False

    def extraer(self, monto):
        """Debita el monto si la cuenta está activa y hay saldo."""
        if self._bloqueada:
            raise CuentaBloqueadaError(
                f"La cuenta {self._numero} está bloqueada"
            )

        if monto > self._saldo:
            raise SaldoInsuficienteError(
                f"Saldo insuficiente en {self._numero}"
            )

        self._saldo -= monto


if __name__ == "__main__":
    # Sí, la jerarquía original viola LSP: la hija lanza una excepción
    # que el padre no lanzaba, en un caso donde el padre prometía
    # funcionar. Cualquier código que reciba una Cuenta y llame
    # extraer() se rompe al recibir una CuentaBloqueada. El bloqueo no
    # es un tipo de cuenta, es un estado por el que la cuenta pasa y
    # del que puede volver: por eso va como atributo, no como subclase.
    cuenta = Cuenta("001-100", 10000)
    cuenta.extraer(3000)
    print(f"Saldo: ${cuenta.saldo()}")

    cuenta.bloquear()

    try:
        cuenta.extraer(1000)
    except CuentaBloqueadaError as error:
        print(f"Error: {error}")

    cuenta.desbloquear()
    cuenta.extraer(1000)
    print(f"Saldo: ${cuenta.saldo()}")
