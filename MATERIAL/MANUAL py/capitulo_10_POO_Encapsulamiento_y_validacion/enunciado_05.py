# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Fecha con dia, mes y anio privados. Validá en el
# __init__: mes entre 1 y 12, año positivo, día entre 1 y 31 (sin
# preocuparte por meses de 30 días ni bisiestos por ahora).
# -------------------------------------------------------------------------


class Fecha:
    def __init__(self, dia, mes, anio):
        # En este ejercicio no usamos setters.
        #
        # Por eso todas las validaciones se realizan directamente en el
        # constructor antes de guardar los valores.
        #
        # Secuencia:
        #
        # Fecha(dia, mes, anio)
        #         ↓
        # __init__()
        #         ↓
        # validar mes
        #         ↓
        # validar año
        #         ↓
        # validar día
        #         ↓
        # guardar _dia, _mes y _anio

        # El mes solamente puede estar entre 1 y 12.
        if not 1 <= mes <= 12:
            raise ValueError("Mes fuera de rango (1-12)")

        # El año debe ser un número positivo.
        if anio <= 0:
            raise ValueError("Año debe ser positivo")

        # En este ejercicio solamente controlamos que el día esté entre
        # 1 y 31.
        #
        # Todavía no verificamos si el mes tiene 28, 30 o 31 días.
        if not 1 <= dia <= 31:
            raise ValueError("Día fuera de rango (1-31)")

        # Los valores se guardan recién después de superar todas las
        # validaciones.
        #
        # Usamos un solo guion bajo (_dia, _mes y _anio) porque Python
        # utiliza esta convención para indicar que son atributos de uso
        # interno de la clase.
        #
        # Técnicamente se podría acceder, por ejemplo, a fecha._dia
        # desde afuera, pero hacerlo significa romper el contrato de la
        # clase.
        #
        # No usamos __dia, __mes o __anio porque el doble guion bajo
        # activa name mangling. Este mecanismo se reserva principalmente
        # para evitar colisiones de nombres en situaciones de herencia.
        self._dia = dia
        self._mes = mes
        self._anio = anio

    def __str__(self):
        # :02d muestra el número entero usando dos posiciones.
        #
        # Por ejemplo:
        #
        # 7  → 07
        # 25 → 25
        return f"{self._dia:02d}/{self._mes:02d}/{self._anio}"


# ---------------------------------------------------------------
# CASO 1: fecha válida
#
# Fecha(25, 7, 2026)
#         ↓
# mes 7 es válido
#         ↓
# año 2026 es positivo
#         ↓
# día 25 está entre 1 y 31
#         ↓
# se guardan los valores
# ---------------------------------------------------------------

fecha = Fecha(25, 7, 2026)

print(fecha)  # 25/07/2026


# ---------------------------------------------------------------
# CASO 2: mes inválido
#
# Fecha(31, 13, 2026)
#         ↓
# 13 no está entre 1 y 12
#         ↓
# ValueError
#
# Las validaciones siguientes ya no se ejecutan porque raise interrumpe
# inmediatamente la ejecución del constructor.
# ---------------------------------------------------------------

try:
    fecha_invalida = Fecha(31, 13, 2026)
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 3: año inválido
#
# El mes supera la primera validación.
# Después se detecta que el año no es positivo.
# ---------------------------------------------------------------

try:
    fecha_invalida = Fecha(10, 5, 0)
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 4: día inválido
#
# El mes y el año son válidos.
# La tercera validación detecta que el día 40 está fuera de rango.
# ---------------------------------------------------------------

try:
    fecha_invalida = Fecha(40, 5, 2026)
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# IMPORTANTE:
#
# Esta fecha pasa las validaciones de ESTE ejercicio:
#
# Fecha(31, 2, 2026)
#
# El día está entre 1 y 31 y el mes entre 1 y 12.
#
# Todavía no estamos verificando cuántos días tiene realmente cada mes.
# Esa será una validación más completa en el ejercicio siguiente.
# ---------------------------------------------------------------

fecha = Fecha(31, 2, 2026)

print(fecha)  # 31/02/2026
