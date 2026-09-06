# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Escribí una función es_primo(n) usando math.sqrt para no probar todos
# los divisores: alcanza con llegar hasta la raíz cuadrada de n. Verificá
# con es_primo(97), que debe dar True, y es_primo(100), que debe dar
# False. Contemplá también los casos n < 2.
# -------------------------------------------------------------------------

import math


def es_primo(n):
    """Devuelve True si n es un número primo."""
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0:
        return False

    # Si n = a * b, alguno de los dos es <= raíz de n. Por eso no
    # hace falta probar divisores más grandes que la raíz.
    limite = int(math.sqrt(n)) + 1

    for divisor in range(3, limite, 2):
        if n % divisor == 0:
            return False

    return True


if __name__ == "__main__":
    for numero in [1, 2, 17, 97, 100, 121]:
        print(f"{numero:>4}: {es_primo(numero)}")
