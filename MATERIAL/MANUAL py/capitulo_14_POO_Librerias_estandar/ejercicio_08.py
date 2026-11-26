# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Extraé los números del texto "El precio es $3.500 y el descuento del
# 15% deja $2.975" usando re.findall. Ojo con el punto: acá es separador
# de miles, no decimal, así que 3.500 son tres mil quinientos.
# -------------------------------------------------------------------------

import re

PATRON_NUMERO = re.compile(r"\d+(?:\.\d+)?")


def extraer_numeros(texto):
    """Devuelve los números que aparecen en el texto, como texto."""
    return PATRON_NUMERO.findall(texto)


if __name__ == "__main__":
    texto = (
        "El precio es $3.500 y el descuento "
        "del 15% deja $2.975"
    )

    numeros = extraer_numeros(texto)
    print(numeros)

    # (?:...) es un grupo que agrupa pero NO captura: sirve para
    # aplicarle el ? a ".\d+" sin que findall devuelva esa parte
    # por separado.
    limpios = [
        float(numero.replace(".", "")) for numero in numeros
    ]
    print(limpios)
