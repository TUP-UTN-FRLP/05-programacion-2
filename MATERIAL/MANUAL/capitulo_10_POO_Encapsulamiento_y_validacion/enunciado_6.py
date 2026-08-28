# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Ampliá la Fecha para que el día valide contra el mes correspondiente
# (30 en abril/junio/septiembre/noviembre, 28 en febrero, 31 en el
# resto). Ignorá bisiestos.
# -------------------------------------------------------------------------


class Fecha:
    def __init__(self, dia, mes, anio):
        if not 1 <= mes <= 12:
            raise ValueError("Mes fuera de rango (1-12)")

        if anio <= 0:
            raise ValueError("Año debe ser positivo")

        # Días máximos según el mes
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

        if not 1 <= dia <= dias_por_mes[mes]:
            raise ValueError(
                f"Día fuera de rango para el mes {mes}"
            )

        self._dia = dia
        self._mes = mes
        self._anio = anio

    def __str__(self):
        return f"{self._dia:02d}/{self._mes:02d}/{self._anio}"


Fecha(31, 4, 2026)  # ValueError (abril tiene 30)

Fecha(29, 2, 2026)  # ValueError (febrero tiene 28, ignoramos bisiestos)
