# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Usá Counter sobre una lista de notas para contar la frecuencia de
# cada una y mostrar cuál fue la más frecuente. Mostrá también el
# histograma completo ordenado por nota.
# -------------------------------------------------------------------------

from collections import Counter


def resumen_de_notas(notas):
    """Devuelve el conteo de notas y la más frecuente."""
    conteo = Counter(notas)
    mas_frecuente, veces = conteo.most_common(1)[0]

    return conteo, mas_frecuente, veces


if __name__ == "__main__":
    notas = [7, 8, 5, 9, 7, 8, 6, 7, 10, 5]

    conteo, mas_frecuente, veces = resumen_de_notas(notas)

    for nota in sorted(conteo):
        print(f"  {nota:>2}: {'#' * conteo[nota]}")

    print(f"La nota más frecuente fue {mas_frecuente} ({veces})")
