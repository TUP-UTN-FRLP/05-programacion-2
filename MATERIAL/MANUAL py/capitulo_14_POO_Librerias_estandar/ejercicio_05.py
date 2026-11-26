# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Dado un CSV con notas de alumnos, con columnas nombre, materia y
# nota, calculá el promedio de cada alumno y guardá el resultado en un
# CSV nuevo. El programa crea primero su propio archivo de entrada.
# -------------------------------------------------------------------------

import csv
from collections import defaultdict


def crear_csv_de_ejemplo(ruta):
    """Genera el CSV de notas con datos de prueba."""
    filas = [
        ("Ana", "Matemática", "8"),
        ("Ana", "Programación", "9"),
        ("Juan", "Matemática", "6"),
        ("Juan", "Programación", "7"),
        ("Pedro", "Matemática", "10"),
    ]

    with open(ruta, "w", newline="", encoding="utf-8") as salida:
        escritor = csv.writer(salida)
        escritor.writerow(["nombre", "materia", "nota"])
        escritor.writerows(filas)


def calcular_promedios(ruta_entrada, ruta_salida):
    """Agrupa las notas por alumno y guarda los promedios."""
    notas_por_alumno = defaultdict(list)

    with open(
        ruta_entrada, newline="", encoding="utf-8"
    ) as archivo:
        for fila in csv.DictReader(archivo):
            notas_por_alumno[fila["nombre"]].append(
                float(fila["nota"])
            )

    with open(
        ruta_salida, "w", newline="", encoding="utf-8"
    ) as salida:
        escritor = csv.writer(salida)
        escritor.writerow(["nombre", "promedio"])

        for nombre, notas in notas_por_alumno.items():
            promedio = sum(notas) / len(notas)
            escritor.writerow([nombre, f"{promedio:.2f}"])

    return notas_por_alumno


if __name__ == "__main__":
    crear_csv_de_ejemplo("notas.csv")
    agrupadas = calcular_promedios("notas.csv", "promedios.csv")

    for nombre, notas in agrupadas.items():
        print(f"  {nombre}: {sum(notas) / len(notas):.2f}")

    print("Promedios guardados en promedios.csv")
