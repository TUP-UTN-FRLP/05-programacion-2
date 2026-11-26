# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Validá si un texto tiene formato de email con una expresión regular.
# Probá con "ana@correo.com" y con "no es email". Tené presente que este
# patrón es una aproximación didáctica: validar emails de verdad es
# mucho más complejo y en un sistema real se valida enviando un correo.
# -------------------------------------------------------------------------

import re

PATRON_EMAIL = re.compile(r"[\w.-]+@[\w.-]+\.\w+")


def es_email(texto):
    """Devuelve True si el texto tiene forma de email."""
    return PATRON_EMAIL.fullmatch(texto) is not None


if __name__ == "__main__":
    for caso in [
        "ana@correo.com",
        "pedro_lopez@ejemplo.com.ar",
        "no es email",
        "arroba@",
    ]:
        print(f"{caso:>28}: {es_email(caso)}")
