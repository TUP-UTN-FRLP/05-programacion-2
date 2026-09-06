# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Escribí dias_hasta_navidad() que devuelva cuántos días faltan para la
# próxima Navidad, el 25 de diciembre. Si la de este año ya pasó, la
# próxima es la del año siguiente.
# -------------------------------------------------------------------------

from datetime import date


def dias_hasta_navidad(hoy=None):
    """Días que faltan para la próxima Navidad."""
    if hoy is None:
        hoy = date.today()

    navidad = date(hoy.year, 12, 25)

    if hoy > navidad:
        navidad = date(hoy.year + 1, 12, 25)

    return (navidad - hoy).days


if __name__ == "__main__":
    print(f"Faltan {dias_hasta_navidad()} días para Navidad")

    # Restar dos date da un timedelta; .days lo da en días enteros.
    print(dias_hasta_navidad(date(2026, 12, 26)))
