# -*- coding: utf-8 -*-
# -----------------------------------------------------
# Enunciado 6:
# Con un diccionario de alumnos que contiene sus datos
# y sus notas, calcular e imprimir el promedio de notas
# de cada alumno.
# -----------------------------------------------------

# Crear el diccionario de alumnos
alumnos = {
    "juan_perez": {
        "nombre": "Juan Pérez",
        "edad": 25,
        "notas": [8, 7, 9]
    },
    "ana_lopez": {
        "nombre": "Ana López",
        "edad": 22,
        "notas": [10, 9, 10]
    }
}

# Recorrer cada alumno y sus datos
for legajo, datos in alumnos.items():

    # Obtener la lista de notas
    notas = datos["notas"]

    # Calcular el promedio
    promedio = sum(notas) / len(notas)

    # Mostrar nombre y promedio
    print(f"{datos['nombre']}: {promedio:.2f}")
