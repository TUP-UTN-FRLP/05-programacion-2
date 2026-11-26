# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Composición uno a muchos: hacé una clase Cuenta con numero y saldo, y
# una clase Cliente con nombre, dni y una lista de Cuenta. Agregá
# abrir_cuenta(numero, saldo_inicial), saldo_total() y
# listar_cuentas(). Las cuentas nacen dentro del cliente: es el cliente
# quien las crea, no se las pasan hechas desde afuera.
# -------------------------------------------------------------------------

class Cuenta:
    """Cuenta simple con número y saldo."""

    def __init__(self, numero, saldo_inicial=0):
        self._numero = numero
        self._saldo = saldo_inicial

    def saldo(self):
        """Devuelve el saldo actual de la cuenta."""
        return self._saldo

    def depositar(self, monto):
        """Suma un monto positivo al saldo."""
        if monto <= 0:
            raise ValueError("El monto debe ser positivo")

        self._saldo += monto

    def __str__(self):
        return f"Cta {self._numero}: ${self._saldo}"


class Cliente:
    """Cliente compuesto por una lista de cuentas propias."""

    def __init__(self, nombre, dni):
        self._nombre = nombre
        self._dni = dni
        self._cuentas = []

    def abrir_cuenta(self, numero, saldo_inicial=0):
        """Crea una cuenta nueva del cliente y la devuelve."""
        cuenta = Cuenta(numero, saldo_inicial)
        self._cuentas.append(cuenta)

        return cuenta

    def saldo_total(self):
        """Suma los saldos de todas las cuentas del cliente."""
        return sum(
            cuenta.saldo() for cuenta in self._cuentas
        )

    def listar_cuentas(self):
        """Imprime el detalle de las cuentas del cliente."""
        print(f"{self._nombre} (DNI {self._dni})")

        for cuenta in self._cuentas:
            print(f"  {cuenta}")

        print(f"  Saldo total: ${self.saldo_total()}")


if __name__ == "__main__":
    cliente = Cliente("Ana Perez", "12345678")
    cliente.abrir_cuenta("001-100", 5000)
    caja = cliente.abrir_cuenta("001-101", 12000)

    caja.depositar(3000)
    cliente.listar_cuentas()
