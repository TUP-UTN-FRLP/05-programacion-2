# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 17
# Función calcular_edad_promedio(personas) donde personas es una
# lista de diccionarios [{"nombre": "Ana", "edad": 25},
# {"nombre": "Juan", "edad": 30}, ...]. Si a alguno le falta la
# clave "edad", ignorarlo. Devolver el promedio de los que sí
# la tienen.
# -------------------------------------------------------------------------


def calcular_edad_promedio(personas):
    edades = []

    for persona in personas:
        # persona["edad"] falla con KeyError si falta esa clave.
        # continue ignora esa persona y pasa a la siguiente.
        try:
            edades.append(persona["edad"])
        except KeyError:
            continue

    if len(edades) == 0:
        return 0

    return sum(edades) / len(edades)


datos = [
    {"nombre": "Ana", "edad": 25},
    {"nombre": "Juan"},
    {"nombre": "Pedro", "edad": 30},
    {"nombre": "Lucía", "edad": 22}
]

print(calcular_edad_promedio(datos))
