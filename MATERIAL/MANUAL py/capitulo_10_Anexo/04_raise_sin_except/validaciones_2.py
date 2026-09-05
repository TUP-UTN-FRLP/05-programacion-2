def validar_stock(valor):
    if not isinstance(valor, int) or isinstance(valor, bool):
        raise TypeError("El stock debe ser int")
    if valor < 0:
        raise ValueError("El stock no puede ser negativo")
    return valor
