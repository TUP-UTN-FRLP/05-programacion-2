def validar_clave(valor):
    if not isinstance(valor, str):
        raise TypeError("La clave debe ser str")
    if len(valor) < 8:
        raise ValueError("La clave debe tener al menos 8 caracteres")
    return valor
