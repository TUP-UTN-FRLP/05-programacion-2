import re


def validar_codigo(valor):
    if not isinstance(valor, str):
        raise TypeError("El codigo debe ser str")
    if not re.match(r"^[A-Z]{3}[0-9]{3}$", valor):
        raise ValueError(f"Codigo invalido: {valor!r}")
    return valor
