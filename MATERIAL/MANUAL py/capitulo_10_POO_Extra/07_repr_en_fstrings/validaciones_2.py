def validar_codigo(valor):
    if not isinstance(valor, str):
        raise TypeError(f"Codigo no textual: {valor!r}")
    if " " in valor:
        raise ValueError(f"El codigo no admite espacios: {valor!r}")
    return valor
