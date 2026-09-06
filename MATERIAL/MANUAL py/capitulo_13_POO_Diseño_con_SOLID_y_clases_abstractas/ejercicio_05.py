# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# DIP: hacé que Banco deje de depender de una implementación concreta
# de almacenamiento. Definí RepositorioCuentas como abstracción y dos
# implementaciones, una en memoria y un doble de prueba. Banco debe
# recibir el repositorio por constructor y no conocer ninguna de las
# dos clases concretas.
# -------------------------------------------------------------------------

from abc import ABC, abstractmethod


class RepositorioCuentas(ABC):
    """Abstracción: algo que sabe guardar y recuperar cuentas."""

    @abstractmethod
    def guardar(self, numero, cuenta):
        """Persiste la cuenta bajo su número."""

    @abstractmethod
    def obtener(self, numero):
        """Devuelve la cuenta o None si no está guardada."""


class RepositorioMemoria(RepositorioCuentas):
    """Implementación real, en memoria."""

    def __init__(self):
        self._datos = {}

    def guardar(self, numero, cuenta):
        self._datos[numero] = cuenta

    def obtener(self, numero):
        return self._datos.get(numero)


class RepositorioFalso(RepositorioCuentas):
    """Doble de prueba: no guarda nada, cuenta las llamadas."""

    def __init__(self):
        self.llamadas_guardar = 0

    def guardar(self, numero, cuenta):
        self.llamadas_guardar += 1

    def obtener(self, numero):
        return None


class Banco:
    """Depende de la abstracción, no de dónde se guardan las cuentas."""

    def __init__(self, repositorio):
        self._repositorio = repositorio

    def abrir_cuenta(self, numero, saldo):
        """Registra una cuenta nueva en el repositorio."""
        self._repositorio.guardar(numero, saldo)

    def saldo_de(self, numero):
        """Devuelve el saldo guardado o None."""
        return self._repositorio.obtener(numero)


if __name__ == "__main__":
    banco = Banco(RepositorioMemoria())
    banco.abrir_cuenta("001-100", 10000)
    print(banco.saldo_de("001-100"))

    # Para probar Banco sin tocar disco ni base de datos, se le inyecta
    # el doble. Banco no cambia una línea.
    falso = RepositorioFalso()
    Banco(falso).abrir_cuenta("001-101", 5000)

    assert falso.llamadas_guardar == 1, "debería guardar una vez"
    print("Banco usa el repositorio inyectado")
