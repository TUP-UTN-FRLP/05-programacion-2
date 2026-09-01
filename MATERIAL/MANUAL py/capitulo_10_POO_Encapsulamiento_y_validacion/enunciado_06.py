# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Ampliá la Fecha para que el día valide contra el mes correspondiente
# (30 en abril/junio/septiembre/noviembre, 28 en febrero, 31 en el
# resto). Ignorá bisiestos.
# -------------------------------------------------------------------------


class Fecha:
    def __init__(self, dia, mes, anio):
        # En este ejercicio seguimos realizando las validaciones
        # directamente dentro del constructor.
        #
        # La diferencia con el ejercicio anterior es que ahora el día no
        # se valida simplemente entre 1 y 31.
        #
        # Primero debemos conocer el mes para saber cuál es el máximo de
        # días permitido.
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
        # buscar cuántos días tiene ese mes
        #         ↓
        # validar el día usando ese máximo
        #         ↓
        # guardar _dia, _mes y _anio

        # Primero validamos el mes.
        #
        # Esto debe hacerse antes de consultar dias_por_mes[mes].
        # Si permitiéramos, por ejemplo, mes = 13, la clave 13 no
        # existiría en el diccionario.
        if not 1 <= mes <= 12:
            raise ValueError("Mes fuera de rango (1-12)")

        # El año debe ser positivo.
        if anio <= 0:
            raise ValueError("Año debe ser positivo")

        # El diccionario relaciona cada número de mes con la cantidad
        # máxima de días que puede tener.
        #
        # Por ejemplo:
        #
        # dias_por_mes[2]  → 28
        # dias_por_mes[4]  → 30
        # dias_por_mes[7]  → 31
        #
        # En este ejercicio ignoramos los años bisiestos, por lo que
        # febrero siempre tiene 28 días.
        dias_por_mes = {
            1: 31,
            2: 28,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31,
        }

        # dias_por_mes[mes] devuelve el máximo permitido para el mes
        # recibido.
        #
        # Por ejemplo, si:
        #
        # mes = 4
        #
        # entonces:
        #
        # dias_por_mes[4]
        #
        # devuelve:
        #
        # 30
        #
        # Por lo tanto, la condición queda conceptualmente:
        #
        # 1 <= dia <= 30
        maximo_dias = dias_por_mes[mes]

        if not 1 <= dia <= maximo_dias:
            raise ValueError(
                f"Día fuera de rango para el mes {mes}"
            )

        # Los valores se guardan solamente después de que todas las
        # validaciones fueron superadas.
        #
        # Usamos un solo guion bajo (_dia, _mes y _anio) porque en
        # Python esta es la convención para indicar que son atributos
        # de uso interno de la clase.
        #
        # Técnicamente se podría acceder, por ejemplo, a fecha._dia
        # desde afuera, pero hacerlo significa romper el contrato de la
        # clase.
        #
        # No usamos __dia, __mes o __anio porque el doble guion bajo
        # activa name mangling. Este mecanismo se utiliza principalmente
        # para evitar colisiones de nombres en situaciones de herencia.
        self._dia = dia
        self._mes = mes
        self._anio = anio

    def __str__(self):
        # :02d muestra los valores enteros usando dos posiciones.
        #
        # Ejemplos:
        #
        # 4  → 04
        # 9  → 09
        # 25 → 25
        return f"{self._dia:02d}/{self._mes:02d}/{self._anio}"


# ---------------------------------------------------------------
# CASO 1: fecha válida
#
# Fecha(25, 4, 2026)
#         ↓
# mes 4 es válido
#         ↓
# año 2026 es positivo
#         ↓
# dias_por_mes[4] devuelve 30
#         ↓
# 25 está entre 1 y 30
#         ↓
# la fecha se crea correctamente
# ---------------------------------------------------------------

fecha = Fecha(25, 4, 2026)

print(fecha)  # 25/04/2026


# ---------------------------------------------------------------
# CASO 2: día inválido para abril
#
# Fecha(31, 4, 2026)
#         ↓
# mes 4 es válido
#         ↓
# dias_por_mes[4] devuelve 30
#         ↓
# se evalúa:
#
# 1 <= 31 <= 30
#
# resultado: False
#         ↓
# ValueError
# ---------------------------------------------------------------

try:
    fecha_invalida = Fecha(31, 4, 2026)
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 3: día inválido para febrero
#
# Fecha(29, 2, 2026)
#         ↓
# dias_por_mes[2] devuelve 28
#         ↓
# 29 supera el máximo permitido
#         ↓
# ValueError
#
# En este ejercicio ignoramos los años bisiestos.
# ---------------------------------------------------------------

try:
    fecha_invalida = Fecha(29, 2, 2026)
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 4: último día válido de febrero
#
# Fecha(28, 2, 2026)
#         ↓
# dias_por_mes[2] devuelve 28
#         ↓
# 28 está dentro del rango permitido
# ---------------------------------------------------------------

fecha = Fecha(28, 2, 2026)

print(fecha)  # 28/02/2026


# ---------------------------------------------------------------
# CASO 5: mes inválido
#
# Esta validación ocurre antes de consultar el diccionario.
#
# Si el mes no está entre 1 y 12, raise detiene inmediatamente el
# constructor.
# ---------------------------------------------------------------

try:
    fecha_invalida = Fecha(10, 13, 2026)
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 6: año inválido
#
# El mes supera la primera validación, pero el año no es positivo.
# ---------------------------------------------------------------

try:
    fecha_invalida = Fecha(10, 5, 0)
except ValueError as error:
    print(f"Error: {error}")
