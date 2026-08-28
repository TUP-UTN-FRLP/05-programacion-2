# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Creá una excepción LimiteExtraccionSuperadoError. Hacé una clase
# Cajero con un _limite_diario privado (por defecto 100000) y un método
# extraer(monto) que rechace si monto > limite_diario.
# -------------------------------------------------------------------------


class LimiteExtraccionSuperadoError(Exception):
    """Se lanza cuando una extracción supera el límite diario."""

    pass


class Cajero:
    def __init__(self, limite_diario=100000):
        # El límite debe ser un valor numérico.
        if type(limite_diario) not in (int, float):
            raise TypeError("El límite debe ser numérico")

        # El límite debe ser mayor que cero.
        if limite_diario <= 0:
            raise ValueError("El límite debe ser positivo")

        # _limite_diario es el atributo interno donde se guarda el valor.
        #
        # Usamos un solo guion bajo porque en Python indica, por
        # convención, que el atributo es de uso interno de la clase.
        # Técnicamente puede accederse desde afuera, pero hacerlo
        # significa romper el contrato de la clase.
        #
        # No usamos __limite_diario porque el doble guion bajo activa
        # name mangling, usado principalmente para evitar colisiones de
        # nombres en situaciones de herencia.
        self._limite_diario = limite_diario

    @property
    def limite_diario(self):
        # limite_diario es una property de solo lectura.
        #
        # Como no existe @limite_diario.setter, el límite puede
        # consultarse desde afuera pero no modificarse directamente.
        return self._limite_diario

    def extraer(self, monto):
        # Secuencia:
        # extraer(monto)
        #         ↓
        # validar que el monto sea numérico
        #         ↓
        # validar que sea positivo
        #         ↓
        # comparar con el límite
        #         ↓
        # aceptar o rechazar la extracción

        if type(monto) not in (int, float):
            raise TypeError("El monto debe ser numérico")

        if monto <= 0:
            raise ValueError("El monto debe ser positivo")

        # Si el monto es válido pero supera el límite permitido,
        # utilizamos una excepción específica del dominio.
        if monto > self._limite_diario:
            raise LimiteExtraccionSuperadoError(
                f"El límite diario es ${self._limite_diario:.2f}"
            )

        # Si llegamos hasta acá, todas las validaciones fueron superadas.
        print(f"Extrayendo ${monto:.2f}...")


# ---------------------------------------------------------------
# CASO 1: creación con el límite predeterminado
#
# Cajero()
#       ↓
# limite_diario = 100000
#       ↓
# valor numérico y positivo
#       ↓
# _limite_diario = 100000
# ---------------------------------------------------------------

cajero = Cajero()

print(f"Límite diario: ${cajero.limite_diario:.2f}")


# ---------------------------------------------------------------
# CASO 2: extracción válida
#
# extraer(50000)
#       ↓
# es numérico
#       ↓
# es positivo
#       ↓
# 50000 <= 100000
#       ↓
# extracción aceptada
# ---------------------------------------------------------------

try:
    cajero.extraer(50000)
except (
    TypeError,
    ValueError,
    LimiteExtraccionSuperadoError,
) as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 3: extracción exactamente igual al límite
#
# El ejercicio rechaza solamente cuando:
# monto > limite_diario
#
# Por lo tanto, extraer exactamente $100000.00 es válido.
# ---------------------------------------------------------------

try:
    cajero.extraer(100000)
except (
    TypeError,
    ValueError,
    LimiteExtraccionSuperadoError,
) as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 4: extracción que supera el límite
#
# extraer(200000)
#       ↓
# monto válido y positivo
#       ↓
# 200000 > 100000
#       ↓
# LimiteExtraccionSuperadoError
# ---------------------------------------------------------------

try:
    cajero.extraer(200000)
except LimiteExtraccionSuperadoError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 5: monto negativo
#
# El tipo es correcto, pero el valor no es válido.
# Por eso se lanza ValueError.
# ---------------------------------------------------------------

try:
    cajero.extraer(-5000)
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 6: monto con tipo incorrecto
# ---------------------------------------------------------------

try:
    cajero.extraer("50000")
except TypeError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 7: intento de modificar el límite desde afuera
#
# cajero.limite_diario = 200000
#       ↓
# Python busca @limite_diario.setter
#       ↓
# no existe
#       ↓
# AttributeError
# ---------------------------------------------------------------

try:
    cajero.limite_diario = 200000
except AttributeError as error:
    print(f"Error: {error}")


# El límite conserva su valor original.
print(f"Límite diario actual: ${cajero.limite_diario:.2f}")


# ---------------------------------------------------------------
# CASO 8: creación con un límite personalizado
# ---------------------------------------------------------------

cajero_especial = Cajero(250000)

print(
    f"Límite diario especial: "
    f"${cajero_especial.limite_diario:.2f}"
)


# ---------------------------------------------------------------
# CASO 9: creación con un límite inválido
# ---------------------------------------------------------------

try:
    cajero_invalido = Cajero(-1000)
except ValueError as error:
    print(f"Error: {error}")
