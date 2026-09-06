def _es_numero(valor):
    # bool es subclase de int: lo excluimos explicitamente.
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)


def validar_numero(valor):
    if not _es_numero(valor):
        raise TypeError("Se esperaba int o float")
    return valor


def validar_saldo_inicial(valor):
    # Reutiliza validar_numero() para el control de tipo.
    valor = validar_numero(valor)
    if valor < 0:
        raise ValueError("El saldo inicial no puede ser negativo")
    return valor
