# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Escribí dias_habiles_entre(inicio, fin) que cuente los días de lunes a
# viernes entre dos fechas date, incluyendo ambos extremos. Recordá que
# weekday() devuelve 0 para lunes y 6 para domingo. Agregale un parámetro
# opcional feriados con una lista de fechas a descontar.
# -------------------------------------------------------------------------

from datetime import date, timedelta


def dias_habiles_entre(inicio, fin, feriados=None):
    """Cuenta los días de lunes a viernes entre dos fechas."""
    if inicio > fin:
        raise ValueError("El inicio debe ser anterior al fin")

    sin_laborar = set(feriados or [])
    dias = 0
    actual = inicio

    while actual <= fin:
        if actual.weekday() < 5 and actual not in sin_laborar:
            dias += 1

        actual += timedelta(days=1)

    return dias


if __name__ == "__main__":
    inicio = date(2026, 1, 1)
    fin = date(2026, 1, 31)

    print(f"Sin feriados: {dias_habiles_entre(inicio, fin)}")

    feriados = [date(2026, 1, 1), date(2026, 1, 2)]
    print(
        f"Con feriados: "
        f"{dias_habiles_entre(inicio, fin, feriados)}"
    )
