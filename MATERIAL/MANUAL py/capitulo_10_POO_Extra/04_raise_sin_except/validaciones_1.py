def validar_edad(valor):
    if not isinstance(valor, int) or isinstance(valor, bool):
        raise TypeError("La edad debe ser int")
    if valor < 0:
        raise ValueError("La edad no puede ser negativa")
    return valor
