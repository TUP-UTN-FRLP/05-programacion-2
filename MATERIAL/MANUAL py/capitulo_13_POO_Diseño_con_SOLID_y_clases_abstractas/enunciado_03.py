# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# OCP: te dan una función procesar_pago(tipo, monto) con if/elif para
# efectivo, tarjeta y transferencia, cada uno con su comisión.
# Reescribila con una ABC MedioDePago y una clase por medio. Después
# agregá Cripto y comprobá que no tuviste que tocar nada de lo anterior.
# -------------------------------------------------------------------------

from abc import ABC, abstractmethod


class MedioDePago(ABC):
    """Abstracción para cualquier medio de pago."""

    @abstractmethod
    def procesar(self, monto):
        """Devuelve el importe final que se cobra al cliente."""

    def nombre(self):
        """Nombre legible del medio de pago."""
        return type(self).__name__


class Efectivo(MedioDePago):
    """Pago en efectivo, sin comisión."""

    def procesar(self, monto):
        return monto


class Tarjeta(MedioDePago):
    """Pago con tarjeta, con 3% de comisión."""

    def procesar(self, monto):
        return monto * 1.03


class Transferencia(MedioDePago):
    """Transferencia bancaria, con 0,5% de comisión."""

    def procesar(self, monto):
        return monto * 1.005


class Cripto(MedioDePago):
    """Medio agregado después: ninguna clase anterior cambió."""

    def procesar(self, monto):
        return monto * 1.01


def cobrar(medios, monto):
    """Cobra el mismo monto por cada medio, sin preguntar tipos."""
    for medio in medios:
        print(f"  {medio.nombre()}: ${medio.procesar(monto):.2f}")


if __name__ == "__main__":
    print("Antes de agregar Cripto:")
    cobrar([Efectivo(), Tarjeta(), Transferencia()], 10000)

    print("Después, con la misma función cobrar():")
    cobrar(
        [Efectivo(), Tarjeta(), Transferencia(), Cripto()],
        10000,
    )
