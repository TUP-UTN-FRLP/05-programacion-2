def validar_promedio(valor):
    if not isinstance(valor, (int, float)) or isinstance(valor, bool):
        raise TypeError("El promedio debe ser int o float")
    if not 0 <= valor <= 10:
        raise ValueError("El promedio debe estar entre 0 y 10")
    return float(valor)
