# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Escribí una función que reciba las coordenadas de dos puntos,
# (x1, y1) y (x2, y2), y devuelva la distancia entre ellos usando
# math.sqrt primero y math.dist después. Verificá con math.isclose que
# dan el mismo resultado.
# -------------------------------------------------------------------------

import math


def distancia_manual(x1, y1, x2, y2):
    """Calcula la distancia con la fórmula euclidiana."""
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def distancia_con_dist(x1, y1, x2, y2):
    """Calcula la misma distancia usando math.dist."""
    return math.dist([x1, y1], [x2, y2])


if __name__ == "__main__":
    d1 = distancia_manual(0, 0, 3, 4)
    d2 = distancia_con_dist(0, 0, 3, 4)

    print(d1)
    print(d2)
    print(math.isclose(d1, d2))

    # math.dist funciona con cualquier dimensión, no solo 2D.
    print(math.dist([1, 2, 3], [4, 5, 6]))
