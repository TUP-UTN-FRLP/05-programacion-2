import re


def validar_patente(valor):
    if not isinstance(valor, str):
        raise TypeError("La patente debe ser str")
    limpio = valor.strip().upper()
    if not re.match(r"^[A-Z]{2}[0-9]{3}[A-Z]{2}$", limpio):
        raise ValueError(f"Patente invalida: {valor!r}")
    return limpio
