def validar_activo(valor):
    if not isinstance(valor, bool):
        raise TypeError("Activo debe ser bool")
    return valor
