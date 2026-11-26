# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 10
# Función convertir_notas(lista_strings) que reciba una lista tipo
# ["7", "8", "abc", "5", "diez", "9"] y devuelva la lista con los
# que sí pudieron convertirse a números, ignorando el resto.
# Ejemplo: [7, 8, 5, 9].
# -------------------------------------------------------------------------


def convertir_notas(lista_strings):
    numeros = []
    for s in lista_strings:
        # int() falla con ValueError si el string no es numérico.
        # continue ignora el elemento inválido y pasa al siguiente.
        try:
            numeros.append(int(s))
        except ValueError:
            continue
    return numeros


datos = ["7", "8", "abc", "5", "diez", "9"]
print(convertir_notas(datos))
