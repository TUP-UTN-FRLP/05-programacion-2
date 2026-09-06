import re


def validar_descripcion(valor):
    if not isinstance(valor, str):
        raise TypeError("La descripcion debe ser str")
    limpio = re.sub(r"\s+", " ", valor).strip()
    if not limpio:
        raise ValueError("La descripcion no puede quedar vacia")
    if len(limpio) > 40:
        raise ValueError("La descripcion no puede superar 40 caracteres")
    return limpio
