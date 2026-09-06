import re


def validar_dni(valor):
    if not isinstance(valor, str):
        raise TypeError("El DNI debe ser str")
    if not re.fullmatch(r"[0-9]{7,8}", valor):
        raise ValueError(
            f"DNI invalido: {valor!r} (se esperan 7 u 8 digitos)"
        )
    return valor
