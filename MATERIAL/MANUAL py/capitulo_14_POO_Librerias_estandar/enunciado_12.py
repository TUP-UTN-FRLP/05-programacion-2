# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Escribí validar_dni(dni) con una expresión regular: debe aceptar
# exactamente 7 u 8 dígitos. Usá re.fullmatch, que exige que el patrón
# cubra toda la cadena, en vez de re.match con ^ y $ al borde. Probá con
# casos válidos e inválidos, incluido un texto con espacios al final.
# -------------------------------------------------------------------------

import re

PATRON_DNI = re.compile(r"\d{7,8}")


def validar_dni(dni):
    """Devuelve True si el DNI tiene exactamente 7 u 8 dígitos."""
    if not isinstance(dni, str):
        return False

    return PATRON_DNI.fullmatch(dni) is not None


if __name__ == "__main__":
    # fullmatch exige que el patrón cubra toda la cadena. Con
    # re.match, "12345678 " daría verdadero si olvidás el $.
    casos = [
        "12345678",
        "1234567",
        "123",
        "12345a78",
        "12345678 ",
        12345678,
    ]

    for caso in casos:
        print(f"{caso!r:>14}: {validar_dni(caso)}")
