def _es_numero(valor):
    # bool es subclase de int: lo excluimos explicitamente.
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def validar_precio(valor):
    if not _es_numero(valor):
        raise TypeError("El precio debe ser int o float")
    if valor < 0:
        raise ValueError("El precio no puede ser negativo")
    return valor
