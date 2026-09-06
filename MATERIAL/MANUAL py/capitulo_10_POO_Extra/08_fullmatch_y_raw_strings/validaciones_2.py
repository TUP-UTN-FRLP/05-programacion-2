import re


def validar_numero_cuenta(valor):
    if not isinstance(valor, str):
        raise TypeError("El numero de cuenta debe ser str")
    if not re.fullmatch(r"[0-9]{14}", valor):
        raise ValueError(
            f"Numero de cuenta invalido: {valor!r} (14 digitos)"
        )
    return valor
