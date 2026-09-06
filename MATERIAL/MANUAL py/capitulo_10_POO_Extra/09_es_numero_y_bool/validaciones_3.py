def _es_numero(valor):
    # bool es subclase de int: lo excluimos explicitamente.
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def validar_temperatura(valor):
    if not _es_numero(valor):
        raise TypeError("La temperatura debe ser int o float")
    if not -100 <= valor <= 100:
        raise ValueError("La temperatura debe estar entre -100 y 100")
    return valor
