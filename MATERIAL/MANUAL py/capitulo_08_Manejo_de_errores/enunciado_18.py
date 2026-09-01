# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 18
# Función dividir_lista(lista, indice) que devuelva
# (parte_izquierda, parte_derecha) cortando en el índice dado.
# Si el índice no es válido, devolver (lista_original, []).
# Usá try/except.
# -------------------------------------------------------------------------


def dividir_lista(lista, indice):
    # lista[:indice] falla con TypeError si el índice no es un entero.
    # El except retorna la lista original junto con [] sin modificarla.
    try:
        return lista[:indice], lista[indice:]
    except TypeError:
        return lista, []


print(dividir_lista([1, 2, 3, 4, 5], 3))
print(dividir_lista([1, 2, 3, 4, 5], "abc"))
