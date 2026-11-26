# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Usá re.sub para anonimizar un texto: reemplazá cada DNI, un grupo de
# 7 u 8 dígitos, por la misma cantidad de X, para no perder la
# información de longitud. Para lograrlo pasale a re.sub una función en
# lugar de una cadena: re.sub la llama con cada coincidencia.
# -------------------------------------------------------------------------

import re

PATRON_DNI = re.compile(r"\b\d{7,8}\b")


def enmascarar(coincidencia):
    """Devuelve tantas X como dígitos tenía el DNI encontrado."""
    return "X" * len(coincidencia.group())


def anonimizar(texto):
    """Reemplaza los DNIs del texto conservando su longitud."""
    return PATRON_DNI.sub(enmascarar, texto)


if __name__ == "__main__":
    texto = (
        "El DNI 12345678 pertenece a Ana. "
        "El DNI 8765432 es de Juan. "
        "El expediente 123 no es un DNI."
    )

    print(anonimizar(texto))

    # \b es un "límite de palabra": impide que 123, con solo tres
    # dígitos, sea tomado como parte de un número más largo.
