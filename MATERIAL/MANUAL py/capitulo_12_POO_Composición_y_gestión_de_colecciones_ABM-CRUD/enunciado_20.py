# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Integrador: armá la iteración 4 del banco. Persona guarda identidad,
# Movimiento registra una operación, Cuenta administra saldo y su
# historial de movimientos, y Banco hace el ABM de cuentas. Cada clase
# tiene una sola responsabilidad y ninguna se mete con las otras.
#
# En un proyecto real esto va en archivos separados: errores.py,
# personas.py, movimientos.py, cuentas.py, banco.py y main.py. Acá está
# todo junto para poder copiarlo de una, pero los comentarios marcan
# dónde estaría el corte de cada módulo.
# -------------------------------------------------------------------------

# --- errores.py ------------------------------------------------

class SaldoInsuficienteError(Exception):
    """Indica que la cuenta no tiene fondos para la operación."""

    pass


class MontoInvalidoError(Exception):
    """Indica que el monto de la operación no es válido."""

    pass


class CuentaNoEncontrada(Exception):
    """Indica que no existe la cuenta solicitada."""

    pass


class NumeroDuplicadoError(Exception):
    """Indica que el número de cuenta ya está usado."""

    pass


# --- personas.py -----------------------------------------------

class Persona:
    """Titular de una cuenta. Solo maneja identidad."""

    def __init__(self, nombre, apellido, dni):
        self._nombre = nombre
        self._apellido = apellido
        self._dni = dni

    def dni(self):
        """Devuelve el documento del titular."""
        return self._dni

    def __str__(self):
        return f"{self._apellido}, {self._nombre}"


# --- movimientos.py --------------------------------------------

class Movimiento:
    """Registro de una operación sobre una cuenta."""

    def __init__(self, tipo, monto, saldo_resultante):
        self._tipo = tipo
        self._monto = monto
        self._saldo_resultante = saldo_resultante

    def __str__(self):
        return (
            f"{self._tipo:<10} ${self._monto:>10} "
            f"-> saldo ${self._saldo_resultante}"
        )


# --- cuentas.py ------------------------------------------------

class Cuenta:
    """Cuenta que administra su saldo y su historial."""

    def __init__(self, numero, titular, saldo=0):
        self._numero = numero
        self._titular = titular
        self._saldo = saldo
        self._movimientos = []

    def numero(self):
        """Devuelve el número de cuenta."""
        return self._numero

    def saldo(self):
        """Devuelve el saldo actual."""
        return self._saldo

    def depositar(self, monto):
        """Acredita un monto positivo y lo registra."""
        if monto <= 0:
            raise MontoInvalidoError(
                "El monto debe ser positivo"
            )

        self._saldo += monto
        self._registrar("depósito", monto)

    def extraer(self, monto):
        """Debita un monto si el saldo alcanza y lo registra."""
        if monto <= 0:
            raise MontoInvalidoError(
                "El monto debe ser positivo"
            )

        if monto > self._saldo:
            raise SaldoInsuficienteError(
                f"Saldo insuficiente en {self._numero}"
            )

        self._saldo -= monto
        self._registrar("extracción", monto)

    def _registrar(self, tipo, monto):
        """Agrega un movimiento al historial de la cuenta."""
        self._movimientos.append(
            Movimiento(tipo, monto, self._saldo)
        )

    def historial(self):
        """Devuelve los movimientos de la cuenta."""
        return list(self._movimientos)

    def __str__(self):
        return (
            f"[{self._numero}] {self._titular} "
            f"- ${self._saldo}"
        )


# --- banco.py --------------------------------------------------

class Banco:
    """Banco que hace el ABM de cuentas. No calcula saldos."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._cuentas = {}

    def abrir_cuenta(self, numero, titular, saldo=0):
        """Da de alta una cuenta nueva y la devuelve."""
        if numero in self._cuentas:
            raise NumeroDuplicadoError(
                f"La cuenta {numero} ya existe"
            )

        cuenta = Cuenta(numero, titular, saldo)
        self._cuentas[numero] = cuenta

        return cuenta

    def buscar(self, numero):
        """Devuelve la cuenta pedida o lanza excepción."""
        cuenta = self._cuentas.get(numero)

        if cuenta is None:
            raise CuentaNoEncontrada(
                f"No existe la cuenta {numero}"
            )

        return cuenta

    def cerrar_cuenta(self, numero):
        """Da de baja física la cuenta indicada."""
        self.buscar(numero)
        del self._cuentas[numero]

    def listar(self):
        """Devuelve todas las cuentas del banco."""
        return list(self._cuentas.values())

    def total_depositado(self):
        """Suma los saldos de todas las cuentas."""
        return sum(
            cuenta.saldo() for cuenta in self.listar()
        )


# --- main.py ---------------------------------------------------

if __name__ == "__main__":
    banco = Banco("Banco de La Plata")

    ana = Persona("Ana", "Pérez", "12345678")
    juan = Persona("Juan", "Gómez", "87654321")

    cuenta_ana = banco.abrir_cuenta("001-100", ana, 10000)
    banco.abrir_cuenta("001-101", juan, 5000)

    cuenta_ana.depositar(2500)
    cuenta_ana.extraer(4000)

    for cuenta in banco.listar():
        print(cuenta)

    print(f"Total depositado: ${banco.total_depositado()}")

    print(f"Historial de {cuenta_ana.numero()}:")
    for movimiento in cuenta_ana.historial():
        print(f"  {movimiento}")

    try:
        cuenta_ana.extraer(999999)
    except SaldoInsuficienteError as error:
        print(f"Error: {error}")

    try:
        banco.buscar("001-999")
    except CuentaNoEncontrada as error:
        print(f"Error: {error}")
