import re


def validar_telefono(valor):
    if not isinstance(valor, str):
        raise TypeError("El telefono debe ser str")
    if not re.fullmatch(r"\+54[0-9]{10}", valor):
        raise ValueError(
            f"Telefono invalido: {valor!r}; usar +54 y 10 digitos"
        )
    return valor
