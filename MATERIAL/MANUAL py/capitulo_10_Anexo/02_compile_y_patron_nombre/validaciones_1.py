import re


# Paso 1: una sola palabra formada por letras (sin espacios ni signos).
_PATRON_NOMBRE = re.compile(r"^[^\W\d_]+$", re.UNICODE)


def validar_nombre(valor):
    if not isinstance(valor, str):
        raise TypeError("El nombre debe ser str")
    limpio = valor.strip()
    if not limpio:
        raise ValueError("El nombre no puede quedar vacio")
    if not _PATRON_NOMBRE.match(limpio):
        raise ValueError(
            f"Nombre con caracteres no permitidos: {valor!r}"
        )
    return limpio.title()
