# -*- coding: utf-8 -*-
# ---------------------------------------------------------
# Enunciado 12:
# Dado el diccionario de notas:
# {"Ana": 8, "Juan": 6, "Pedro": 9, "Lucía": 7, "Diego": 4}
# Mostrar solamente los alumnos con nota mayor o igual a 7.
# ---------------------------------------------------------


# Crear el diccionario de notas
notas = {
    "Ana": 8,
    "Juan": 6,
    "Pedro": 9,
    "Lucía": 7,
    "Diego": 4
}

# Mostrar solamente los alumnos aprobados
print("Aprobados:")

# Recorrer nombres y notas
for nombre, nota in notas.items():

    # Filtrar las notas mayores o iguales a 7
    if nota >= 7:
        print(f"  {nombre}: {nota}")
