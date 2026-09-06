# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Simulá el lanzamiento de un dado de 6 caras 10.000 veces y contá
# cuántas veces salió cada número con Counter. Fijá random.seed(42) antes
# de empezar, para que la simulación dé siempre lo mismo y puedas
# comparar tu resultado con el de un compañero. Verificá que las
# frecuencias sean parejas, alrededor de 1666 cada una.
# -------------------------------------------------------------------------

import random
from collections import Counter

TIRADAS = 10_000


def simular_dado(tiradas):
    """Devuelve el conteo de caras tras lanzar un dado n veces."""
    resultados = [
        random.randint(1, 6) for _ in range(tiradas)
    ]

    return Counter(resultados)


if __name__ == "__main__":
    # La semilla hace la simulación reproducible: mismo seed,
    # misma secuencia. En producción no se fija.
    random.seed(42)

    conteo = simular_dado(TIRADAS)

    for cara in range(1, 7):
        porcentaje = conteo[cara] / TIRADAS * 100
        print(f"{cara}: {conteo[cara]:>5} ({porcentaje:.2f}%)")

    print(f"Esperado por cara: {TIRADAS / 6:.0f} (16.67%)")
