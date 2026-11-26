def validar_observacion(valor):
    if not isinstance(valor, str):
        raise TypeError(f"La observacion debe ser str: {valor!r}")
    if valor != valor.strip():
        raise ValueError(
            f"La observacion tiene espacios en los extremos: {valor!r}"
        )
    return valor
