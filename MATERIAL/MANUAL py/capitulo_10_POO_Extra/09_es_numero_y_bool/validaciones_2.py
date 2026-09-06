def _es_numero(valor):
    # bool es subclase de int: lo excluimos explicitamente.
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def validar_altura(valor):
    if not _es_numero(valor):
        raise TypeError("La altura debe ser int o float")
    if valor <= 0:
        raise ValueError("La altura debe ser mayor que cero")
    return float(valor)
