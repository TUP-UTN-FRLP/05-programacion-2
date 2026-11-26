# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Escribí contar_archivos_por_extension(carpeta), que reciba un Path a
# una carpeta y devuelva un diccionario {extensión: cantidad} con los
# archivos de cada tipo. Usá Counter para no tener que inicializar las
# claves a mano.
# -------------------------------------------------------------------------

from collections import Counter
from pathlib import Path


def contar_archivos_por_extension(carpeta):
    """Cuenta los archivos directos agrupados por extensión."""
    contador = Counter(
        item.suffix
        for item in carpeta.iterdir()
        if item.is_file()
    )

    return dict(contador)


if __name__ == "__main__":
    resultado = contar_archivos_por_extension(Path("."))

    for extension, cantidad in sorted(resultado.items()):
        nombre = extension or "(sin extensión)"
        print(f"  {nombre}: {cantidad}")
