# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Limpiá un texto que tiene espacios, saltos de línea y tabulaciones
# repetidos, para obtener "Ana María Pérez". Usá re.sub para colapsar
# todos los blancos consecutivos en uno solo, y strip para los extremos.
# -------------------------------------------------------------------------

import re

PATRON_BLANCOS = re.compile(r"\s+")


def limpiar_espacios(texto):
    """Colapsa los blancos consecutivos y recorta los extremos."""
    return PATRON_BLANCOS.sub(" ", texto).strip()


if __name__ == "__main__":
    sucio = "   Ana    María \n\n\t  Pérez   "

    print(repr(sucio))
    print(repr(limpiar_espacios(sucio)))

    # \s cubre espacio, tabulación y salto de línea; el + exige
    # una o más repeticiones seguidas.
