# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# math más allá de la raíz. Escribí altura_por_angulo(distancia, grados),
# que calcule la altura de un edificio a partir de la distancia al pie y
# del ángulo de elevación, y magnitud_relativa(energia_1, energia_2), que
# devuelva cuántos órdenes de magnitud separan dos energías usando
# log10. Acordate de que las funciones trigonométricas trabajan en
# radianes: hay que convertir con math.radians.
# -------------------------------------------------------------------------

import math


def altura_por_angulo(distancia, grados):
    """Altura de un objeto según distancia y ángulo de elevación."""
    if not 0 < grados < 90:
        raise ValueError("El ángulo debe estar entre 0 y 90")

    return distancia * math.tan(math.radians(grados))


def magnitud_relativa(energia_1, energia_2):
    """Órdenes de magnitud que separan dos energías."""
    if energia_1 <= 0 or energia_2 <= 0:
        raise ValueError("Las energías deben ser positivas")

    return math.log10(energia_2 / energia_1)


if __name__ == "__main__":
    altura = altura_por_angulo(50, 30)
    print(f"Altura estimada: {altura:.2f} m")

    # tan(45°) vale exactamente 1, así que a 45 grados la altura
    # iguala a la distancia. Sirve para comprobar la función.
    print(math.isclose(altura_por_angulo(50, 45), 50))

    ordenes = magnitud_relativa(1_000, 1_000_000)
    print(f"Diferencia: {ordenes:.0f} órdenes de magnitud")

    # Los float no son exactos: 0.1 + 0.2 no da 0.3 porque en
    # binario esos decimales son periódicos. Por eso se compara
    # con math.isclose y no con ==.
    print(0.1 + 0.2 == 0.3)
    print(math.isclose(0.1 + 0.2, 0.3))
