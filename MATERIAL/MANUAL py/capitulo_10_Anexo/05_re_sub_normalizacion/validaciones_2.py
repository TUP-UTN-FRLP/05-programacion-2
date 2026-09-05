import re


def validar_domicilio(valor):
    if not isinstance(valor, str):
        raise TypeError("El domicilio debe ser str")
    limpio = re.sub(r"\s+", " ", valor).strip()
    if not limpio:
        raise ValueError("El domicilio no puede quedar vacio")
    return limpio
