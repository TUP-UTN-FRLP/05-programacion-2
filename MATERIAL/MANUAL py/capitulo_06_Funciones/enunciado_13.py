# -*- coding: utf-8 -*-
# -------------------------------------------------------
# Enunciado 13:
# Escribí una función filtrar_por_letra(nombres, letra)
# que reciba una lista de nombres y devuelva solo los que
# empiezan con la letra dada.
# -------------------------------------------------------


def filtrar_por_letra(nombres, letra):
    resultado = []

    for n in nombres:
        if n.lower().startswith(letra.lower()):
            resultado.append(n)

    return resultado


alumnos = ["Ana", "Bruno", "Andrés", "Carlos", "Alicia"]

print(filtrar_por_letra(alumnos, "A"))
