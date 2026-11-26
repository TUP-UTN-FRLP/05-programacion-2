# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Simulá 1000 tiradas de dos dados. Contá cuántas veces sale doble, es
# decir dos números iguales, y calculá el porcentaje. Fijá la semilla
# con random.seed para que el resultado sea reproducible.
# -------------------------------------------------------------------------

import random

TIRADAS = 1000


def contar_dobles(tiradas):
    """Cuenta cuántas veces salen dos dados iguales."""
    dobles = 0

    for _ in range(tiradas):
        if random.randint(1, 6) == random.randint(1, 6):
            dobles += 1

    return dobles


if __name__ == "__main__":
    random.seed(42)

    dobles = contar_dobles(TIRADAS)
    porcentaje = dobles / TIRADAS * 100

    print(f"Dobles: {dobles} ({porcentaje:.2f}%)")
    print("Probabilidad teórica: 16.67% (1/6)")
