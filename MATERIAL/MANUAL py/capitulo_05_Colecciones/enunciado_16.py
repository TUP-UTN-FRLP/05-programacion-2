# -*- coding: utf-8 -*-
# ---------------------------------------------------------
# Enunciado 16:
# Dada una lista de alumnos con sus notas como diccionarios
# anidados:
# Ana:
# Matemática: 8
# Programación: 9
# Física: 7
# Juan:
# Matemática: 6
# Programación: 8
# Física: 5
# Pedro:
# Matemática: 10
# Programación: 7
# Física: 9
# Calcular el promedio de cada alumno y mostrar cuál tiene
# el mejor promedio.
# ---------------------------------------------------------

# Crear el diccionario de alumnos con diccionarios anidados
alumnos = {
    "Ana": {
        "Matemática": 8,
        "Programación": 9,
        "Física": 7
    },
    "Juan": {
        "Matemática": 6,
        "Programación": 8,
        "Física": 5
    },
    "Pedro": {
        "Matemática": 10,
        "Programación": 7,
        "Física": 9
    }
}

# Variables para guardar el mejor resultado encontrado
mejor_alumno = ""
mejor_promedio = 0

# Recorrer cada alumno y sus materias
for nombre, materias in alumnos.items():

    # Calcular el promedio usando las notas del diccionario interno
    promedio = sum(materias.values()) / len(materias)

    # Mostrar el promedio del alumno
    print(f"{nombre}: {promedio:.2f}")

    # Comprobar si es el mejor promedio encontrado hasta ahora
    if promedio > mejor_promedio:
        mejor_promedio = promedio
        mejor_alumno = nombre

# Mostrar el alumno con mejor promedio
print(f"\nMejor alumno: {mejor_alumno} "
      f"con promedio {mejor_promedio:.2f}")
