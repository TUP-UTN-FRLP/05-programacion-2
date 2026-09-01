# -*- coding: utf-8 -*-
# ------------------------------------------------------------------
# Enunciado 6:
# Dado el diccionario {"Ana": 8, "Juan": 6, "Pedro": 9, "Lucía": 7},
# imprimir el nombre y la nota de cada alumno,
# y calcular el promedio del curso.
# Funciones sugeridas: .items(), .values()
# ------------------------------------------------------------------


# Crear el diccionario de notas
notas = {
    "Ana": 8,
    "Juan": 6,
    "Pedro": 9,
    "Lucía": 7
}

# Recorrer el diccionario obteniendo nombre y nota
for nombre, nota in notas.items():
    print(f"{nombre}: {nota}")

# Calcular el promedio utilizando solamente los valores
promedio = sum(notas.values()) / len(notas)

# Mostrar el promedio con dos decimales
print(f"Promedio del curso: {promedio:.2f}")
