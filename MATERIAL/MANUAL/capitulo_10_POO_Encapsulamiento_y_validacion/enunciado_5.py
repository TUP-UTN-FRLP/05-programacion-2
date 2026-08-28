# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Fecha con dia, mes y anio privados. Validá en el
# __init__: mes entre 1 y 12, año positivo, día entre 1 y 31 (sin
# preocuparte por meses de 30 días ni bisiestos por ahora).
# -------------------------------------------------------------------------


class Fecha:
    def __init__(self, dia, mes, anio):
        if not 1 <= mes <= 12:
            raise ValueError("Mes fuera de rango (1-12)")

        if anio <= 0:
            raise ValueError("Año debe ser positivo")

        if not 1 <= dia <= 31:
            raise ValueError("Día fuera de rango (1-31)")

        self._dia = dia
        self._mes = mes
        self._anio = anio

    def __str__(self):
        return f"{self._dia:02d}/{self._mes:02d}/{self._anio}"


f = Fecha(25, 7, 2026)

print(f)  # 25/07/2026

Fecha(31, 13, 2026)  # ValueError
