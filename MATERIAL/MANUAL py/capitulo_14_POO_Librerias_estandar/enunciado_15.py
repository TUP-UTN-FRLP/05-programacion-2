# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Dada una lista de tuplas (alumno, materia, nota), agrupá las notas por
# alumno con defaultdict(list) y mostrá el promedio de cada uno, ordenado
# de mayor a menor. Compará con lo que habría que escribir usando un dict
# normal y anotalo en un comentario.
# -------------------------------------------------------------------------

from collections import defaultdict


def agrupar_notas(registros):
    """Agrupa las notas de cada alumno en un diccionario."""
    por_alumno = defaultdict(list)

    for alumno, _materia, nota in registros:
        por_alumno[alumno].append(nota)

    return dict(por_alumno)


def promedios_ordenados(por_alumno):
    """Devuelve (alumno, promedio) de mayor a menor promedio."""
    promedios = [
        (alumno, sum(notas) / len(notas))
        for alumno, notas in por_alumno.items()
    ]

    return sorted(promedios, key=lambda par: par[1], reverse=True)


if __name__ == "__main__":
    # Con un dict normal habría que escribir, en cada vuelta:
    #     if alumno not in por_alumno:
    #         por_alumno[alumno] = []
    # defaultdict(list) hace exactamente eso, automáticamente.
    registros = [
        ("Ana", "Matemática", 8),
        ("Ana", "Programación", 9),
        ("Juan", "Matemática", 6),
        ("Juan", "Programación", 7),
        ("Ana", "Física", 7),
        ("Pedro", "Matemática", 10),
    ]

    agrupadas = agrupar_notas(registros)

    for alumno, promedio in promedios_ordenados(agrupadas):
        print(f"  {alumno}: {promedio:.2f}")
