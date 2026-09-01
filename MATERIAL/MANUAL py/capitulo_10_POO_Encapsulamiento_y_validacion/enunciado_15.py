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
        # Todas las validaciones se realizan antes de guardar los datos.
        #
        # Secuencia:
        # Tarjeta(numero, mes_vencimiento, anio_vencimiento)
        #         ↓
        # validar número
        #         ↓
        # validar mes
        #         ↓
        # obtener fecha actual
        #         ↓
        # verificar vencimiento
        #         ↓
        # guardar los atributos internos

        # El número se recibe como string porque no vamos a realizar
        # operaciones matemáticas con él y podría comenzar con cero.
        #
        # Debe cumplir tres condiciones:
        # - ser un string;
        # - tener exactamente 16 caracteres;
        # - contener solamente dígitos.
        if not (
            isinstance(numero, str)
            and len(numero) == 16
            and numero.isdigit()
        ):
            raise ValueError(
                "Número inválido: debe ser 16 dígitos"
            )

        # El mes de vencimiento debe estar entre 1 y 12.
        if not 1 <= mes_vencimiento <= 12:
            raise ValueError("Mes fuera de rango (1-12)")

        # datetime.now() devuelve la fecha y hora actuales.
        # De ese objeto utilizamos:
        # hoy.year  → año actual
        # hoy.month → mes actual
        hoy = datetime.now()

        # Una tarjeta está vencida en dos situaciones:
        #
        # 1. El año de vencimiento es anterior al año actual.
        #
        # 2. El año es el actual, pero el mes de vencimiento ya pasó.
        #
        # Si vence durante el mes actual todavía se considera válida.
        if anio_vencimiento < hoy.year or (
            anio_vencimiento == hoy.year
            and mes_vencimiento < hoy.month
        ):
            raise TarjetaVencidaError(
                f"Tarjeta vencida en "
                f"{mes_vencimiento}/{anio_vencimiento}"
            )

        # Los datos se guardan solamente después de superar todas las
        # validaciones.
        #
        # Usamos un solo guion bajo porque en Python indica, por
        # convención, que estos atributos son de uso interno de la clase.
        # Técnicamente pueden accederse desde afuera, pero hacerlo
        # significa romper el contrato de la clase.
        #
        # No usamos __numero, __mes_vencimiento o __anio_vencimiento
        # porque el doble guion bajo activa name mangling, utilizado
        # principalmente para evitar colisiones de nombres en herencia.
        self._numero = numero
        self._mes_vencimiento = mes_vencimiento
        self._anio_vencimiento = anio_vencimiento


# Obtenemos la fecha actual para que las pruebas sigan funcionando con
# el paso de los años.
hoy = datetime.now()


# ---------------------------------------------------------------
# CASO 1: tarjeta válida
#
# Usamos el mes y año actuales.
#
# Una tarjeta que vence durante el mes actual todavía es válida.
# ---------------------------------------------------------------

try:
    tarjeta = Tarjeta(
        "1234567812345678",
        hoy.month,
        hoy.year,
    )
    print("Tarjeta válida")
except (ValueError, TarjetaVencidaError) as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 2: número de tarjeta inválido
#
# "1234"
#       ↓
# es un string
#       ↓
# pero no tiene 16 caracteres
#       ↓
# ValueError
# ---------------------------------------------------------------

try:
    tarjeta = Tarjeta(
        "1234",
        hoy.month,
        hoy.year,
    )
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 3: número con caracteres que no son dígitos
#
# isdigit() devuelve False.
# ---------------------------------------------------------------

try:
    tarjeta = Tarjeta(
        "12345678ABCDEFGH",
        hoy.month,
        hoy.year,
    )
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 4: mes inválido
#
# mes_vencimiento = 13
#       ↓
# no está entre 1 y 12
#       ↓
# ValueError
# ---------------------------------------------------------------

try:
    tarjeta = Tarjeta(
        "1234567812345678",
        13,
        hoy.year,
    )
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 5: tarjeta vencida
#
# Utilizamos el año anterior para garantizar que la tarjeta esté
# vencida independientemente del mes actual.
#
# año anterior < año actual
#       ↓
# TarjetaVencidaError
# ---------------------------------------------------------------

try:
    tarjeta = Tarjeta(
        "1234567812345678",
        12,
        hoy.year - 1,
    )
except TarjetaVencidaError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 6: tarjeta que vence en el futuro
#
# Un año posterior al actual supera la validación de vencimiento.
# ---------------------------------------------------------------

try:
    tarjeta = Tarjeta(
        "1234567812345678",
        1,
        hoy.year + 1,
    )
    print("Tarjeta futura válida")
except (ValueError, TarjetaVencidaError) as error:
    print(f"Error: {error}")
