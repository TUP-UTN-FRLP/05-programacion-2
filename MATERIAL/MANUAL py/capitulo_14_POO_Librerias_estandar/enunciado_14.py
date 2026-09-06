# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Contá las palabras más frecuentes de un texto usando Counter. Antes de
# contar, pasá todo a minúsculas y quitá los signos de puntuación con
# re.sub. Sacá además las palabras vacías más comunes, como artículos y
# preposiciones, para que el resultado sea informativo.
# -------------------------------------------------------------------------

import re
from collections import Counter

VACIAS = {"la", "el", "y", "de", "a", "es", "un", "una"}


def palabras_frecuentes(texto, cantidad=5, vacias=VACIAS):
    """Devuelve las palabras más frecuentes, sin las vacías."""
    limpio = re.sub(r"[^\w\s]", "", texto.lower())

    palabras = [
        palabra
        for palabra in limpio.split()
        if palabra not in vacias
    ]

    return Counter(palabras).most_common(cantidad)


if __name__ == "__main__":
    texto = (
        "La casa es grande y la casa es blanca. "
        "El perro corre y el perro ladra. "
        "Ana ama a Juan. Juan ama a Ana. "
        "La casa de Ana."
    )

    for palabra, cantidad in palabras_frecuentes(texto):
        print(f"  {palabra}: {cantidad}")
