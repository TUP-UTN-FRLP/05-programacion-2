def validar_nombre_corto(valor):
    if not isinstance(valor, str):
        raise TypeError(f"Se esperaba str y se recibio: {valor!r}")
    limpio = valor.strip()
    if len(limpio) < 2:
        raise ValueError(f"Nombre demasiado corto: {valor!r}")
    return limpio
