# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Pago con monto y un método abstracto conceptual
# procesar(). Hacé las hijas PagoEfectivo, PagoTarjeta y
# PagoTransferencia, cada una con su lógica propia de procesar().
# Recorré una lista mixta de pagos y procesalos todos con un solo bucle.
# -------------------------------------------------------------------------

class Pago:
    """Pago base cuyo procesamiento implementan sus hijas."""

    def __init__(self, monto):
        self._monto = monto

    def procesar(self):
        """Contrato que todo medio de pago debe cumplir."""
        raise NotImplementedError(
            f"La clase {type(self).__name__} debe implementar procesar()"
        )


class PagoEfectivo(Pago):
    """Pago realizado en efectivo."""

    def procesar(self):
        print(f"[EFECTIVO] ${self._monto} recibidos")


class PagoTarjeta(Pago):
    """Pago con tarjeta que agrega una comisión del 3%."""

    def procesar(self):
        comision = self._monto * 0.03
        print(
            f"[TARJETA] ${self._monto} "
            f"+ ${comision:.2f} de comisión"
        )


class PagoTransferencia(Pago):
    """Pago realizado mediante transferencia bancaria."""

    def procesar(self):
        print(
            f"[TRANSFERENCIA] ${self._monto} "
            f"acreditados a las 24hs"
        )


pagos = [
    PagoEfectivo(5000),
    PagoTarjeta(10000),
    PagoTransferencia(20000),
]

for pago in pagos:
    pago.procesar()
