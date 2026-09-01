# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 3
# Escribí una función dividir_seguro(a, b) que devuelva a / b, o
# None si b es cero. Usá try/except.
# -------------------------------------------------------------------------


def dividir_seguro(a, b):
    # a / b falla con ZeroDivisionError si b es cero.
    # El except captura ese caso y retorna None en lugar de propagar el error.
    try:
        return a / b
    except ZeroDivisionError:
        return None


print(dividir_seguro(10, 2))
print(dividir_seguro(10, 0))
