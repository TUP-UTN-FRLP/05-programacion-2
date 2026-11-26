def validar_legajo(valor):
    if not isinstance(valor, int) or isinstance(valor, bool):
        raise TypeError("El legajo debe ser int")
    if valor <= 0:
        raise ValueError("El legajo debe ser positivo")
    return valor
