# -*- coding: utf-8 -*-
# -------------------------------------------------------
# Enunciado 4:
# Crear un diccionario con tu nombre, edad, carrera y año
# en el que cursás.
# Imprimirlo con f-string en una frase legible.
# -------------------------------------------------------

# Crear el diccionario con los datos del alumno
alumno = {
    "nombre": "Sergio",
    "edad": 42,
    "carrera": "Ingeniería en Sistemas",
    "anio": 4
}

# Mostrar los datos en una frase utilizando f-string
print(f"{alumno['nombre']} tiene {alumno['edad']} años, "
      f"cursa {alumno['carrera']} y está en {alumno['anio']}° año.")
