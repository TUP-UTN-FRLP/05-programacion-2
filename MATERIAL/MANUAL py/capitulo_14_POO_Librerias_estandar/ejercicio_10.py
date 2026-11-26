# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Escribí formatear_telefono(numero), que reciba un teléfono en
# cualquier formato, como 2211234567, 221-123-4567 o 221 1234567, y
# devuelva siempre 221-123-4567. La estrategia es normalizar primero,
# quitando todo lo que no sea dígito, y reformatear después.
# -------------------------------------------------------------------------

import re

PATRON_NO_DIGITO = re.compile(r"\D")


def formatear_telefono(numero):
    """Normaliza un teléfono de diez dígitos al formato estándar."""
    solo_digitos = PATRON_NO_DIGITO.sub("", numero)

    if len(solo_digitos) != 10:
        raise ValueError(
            f"Se esperaban 10 dígitos, hay {len(solo_digitos)}"
        )

    return (
        f"{solo_digitos[:3]}-"
        f"{solo_digitos[3:6]}-"
        f"{solo_digitos[6:]}"
    )


if __name__ == "__main__":
    # Normalizar y después reformatear es mucho más simple que
    # armar un regex que contemple todos los formatos posibles.
    for caso in ["2211234567", "221-123-4567", "221 1234567"]:
        print(formatear_telefono(caso))

    try:
        formatear_telefono("221-123")
    except ValueError as error:
        print(f"Error: {error}")
