import re


# Mismo criterio de letras que el bloque 2, permitiendo espacios entre palabras.
_PATRON_CIUDAD = re.compile(r"^[^\W\d_]+(?: [^\W\d_]+)*$", re.UNICODE)


def validar_ciudad(valor):
    if not isinstance(valor, str):
        raise TypeError("La ciudad debe ser str")
    limpio = re.sub(r"\s+", " ", valor).strip()
    if not _PATRON_CIUDAD.match(limpio):
        raise ValueError(f"Ciudad invalida: {valor!r}")
    return limpio
