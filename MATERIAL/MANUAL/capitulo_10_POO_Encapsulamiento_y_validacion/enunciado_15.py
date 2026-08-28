# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Creá una excepción TarjetaVencidaError. Hacé una clase Tarjeta con
# numero (16 dígitos, solo dígitos), mes_vencimiento (1-12) y
# anio_vencimiento (posterior o igual al actual). El __init__ debe
# rechazar tarjetas vencidas con la excepción propia (usá
# datetime.now().year y datetime.now().month).
# -------------------------------------------------------------------------

from datetime import datetime


class TarjetaVencidaError(Exception):
    """Se lanza cuando la tarjeta está fuera de fecha de validez."""

    pass


class Tarjeta:
    def __init__(self, numero, mes_vencimiento, anio_vencimiento):
        if not (
            isinstance(numero, str)
            and len(numero) == 16
            and numero.isdigit()
        ):
            raise ValueError(
                "Número inválido: debe ser 16 dígitos"
            )

        if not 1 <= mes_vencimiento <= 12:
            raise ValueError("Mes fuera de rango")

        hoy = datetime.now()

        if anio_vencimiento < hoy.year or (
            anio_vencimiento == hoy.year
            and mes_vencimiento < hoy.month
        ):
            raise TarjetaVencidaError(
                f"Tarjeta vencida en "
                f"{mes_vencimiento}/{anio_vencimiento}"
            )

        self._numero = numero
        self._mes_vencimiento = mes_vencimiento
        self._anio_vencimiento = anio_vencimiento


Tarjeta("1234567812345678", 12, 2027)  # OK

Tarjeta("1234", 12, 2027)  # ValueError (números)

Tarjeta("1234567812345678", 1, 2020)  # TarjetaVencidaError
