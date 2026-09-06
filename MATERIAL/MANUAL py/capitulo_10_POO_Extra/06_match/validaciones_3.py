import re


_PATRON_ALIAS = re.compile(r"^[a-z][a-z0-9.]{2,14}$")


def validar_alias(valor):
    if not isinstance(valor, str):
        raise TypeError("El alias debe ser str")
    if not _PATRON_ALIAS.match(valor):
        raise ValueError(f"Alias invalido: {valor!r}")
    return valor
