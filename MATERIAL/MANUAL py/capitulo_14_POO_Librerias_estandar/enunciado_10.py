# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Dado un JSON con la estructura
# {"alumnos": [{"nombre": ..., "notas": [...]}, ...]}, calculá el
# promedio de cada alumno y el promedio general del colegio. El programa
# debe crear primero el JSON de ejemplo y después procesarlo.
# -------------------------------------------------------------------------

import json


def crear_json_de_ejemplo(ruta):
    """Genera el archivo de entrada con datos de prueba."""
    colegio = {
        "alumnos": [
            {"nombre": "Ana", "notas": [8, 9, 7]},
            {"nombre": "Juan", "notas": [6, 7, 5]},
            {"nombre": "Pedro", "notas": [10, 9, 10]},
        ]
    }

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(colegio, archivo, indent=2, ensure_ascii=False)


def promedios(ruta):
    """Devuelve los promedios por alumno y el promedio general."""
    with open(ruta, encoding="utf-8") as archivo:
        datos = json.load(archivo)

    por_alumno = {
        alumno["nombre"]: sum(alumno["notas"]) / len(alumno["notas"])
        for alumno in datos["alumnos"]
    }

    todas = [
        nota
        for alumno in datos["alumnos"]
        for nota in alumno["notas"]
    ]

    return por_alumno, sum(todas) / len(todas)


if __name__ == "__main__":
    crear_json_de_ejemplo("colegio.json")

    por_alumno, general = promedios("colegio.json")

    for nombre, promedio in por_alumno.items():
        print(f"  {nombre}: {promedio:.2f}")

    print(f"Promedio general: {general:.2f}")
