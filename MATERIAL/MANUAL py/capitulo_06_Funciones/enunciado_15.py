# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Enunciado 15:
# Escribí una función ordenar_alumnos(alumnos) que reciba
# un diccionario {nombre: nota} y devuelva una lista de tuplas
# (nombre, nota) ordenada de mayor a menor nota.
# Usá sorted() con key=lambda.
# ------------------------------------------------------------


def ordenar_alumnos(alumnos):
    return sorted(
        alumnos.items(),
        key=lambda par: par[1],
        reverse=True
    )


notas = {
    "Ana": 8,
    "Juan": 6,
    "Pedro": 9,
    "Lucía": 7
}

print(ordenar_alumnos(notas))
