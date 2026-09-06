import re


_PATRON_NOMBRE = re.compile(
    r"^[^\W\d_]+(?:[ '\-][^\W\d_]+)*$",
    re.UNICODE,
)


def validar_nombre(valor):
    if not isinstance(valor, str):
        raise TypeError("El nombre debe ser str")
    limpio = re.sub(r"\s+", " ", valor).strip()
    if not limpio:
        raise ValueError("El nombre no puede quedar vacio")
    if not _PATRON_NOMBRE.match(limpio):
        raise ValueError(
            f"Nombre con caracteres no permitidos: {valor!r}"
        )
    return limpio.title()


def validar_apellido(valor):
    # Reutilizamos la misma regla utilizada para nombres.
    return validar_nombre(valor)
