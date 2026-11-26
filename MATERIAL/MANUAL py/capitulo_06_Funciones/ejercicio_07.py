# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------
# Escribí duplicar(lista) que devuelva una lista nueva con cada elemento
# multiplicado por 2, sin modificar la original.
# -----------------------------------------------------------------------


def duplicar(lista):
    resultado = []
    for x in lista:
        resultado.append(x * 2)
    return resultado


originales = [1, 2, 3, 4]
dobles = duplicar(originales)

print(f"Original: {originales}")
print(f"Dobles: {dobles}")
