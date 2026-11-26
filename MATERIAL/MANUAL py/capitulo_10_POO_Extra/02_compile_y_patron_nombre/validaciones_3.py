import re


# Paso 3: ademas del espacio se aceptan apostrofo y guion como separadores.
_PATRON_NOMBRE = re.compile(r"^[^\W\d_]+(?:[ '\-][^\W\d_]+)*$", re.UNICODE)


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
