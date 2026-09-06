import re


def validar_usuario(valor):
    if not isinstance(valor, str):
        raise TypeError("El usuario debe ser str")
    if not re.match(r"^[a-z][a-z0-9_]{4,11}$", valor):
        raise ValueError(f"Usuario invalido: {valor!r}")
    return valor
