def _es_numero(valor):
    # bool es subclase de int: lo excluimos explicitamente.
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def validar_monto(valor):
    if not _es_numero(valor):
        raise TypeError("El monto debe ser int o float")
    if valor <= 0:
        raise ValueError("El monto debe ser mayor que cero")
    return valor


def validar_limite_extraccion(valor):
    valor = validar_monto(valor)
    if valor > 500000:
        raise ValueError("El limite no puede superar 500000")
    return valor
