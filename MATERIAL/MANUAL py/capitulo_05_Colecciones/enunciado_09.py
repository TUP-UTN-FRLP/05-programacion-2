# -*- coding: utf-8 -*-
# ----------------------------------------------------
# Enunciado 9:
# Pedir 5 palabras y determinar si todas son distintas
# o hay repetidas.
# Pista:
# Comparar len() de la lista con len() del set.
# ----------------------------------------------------


# Crear una lista vacía para guardar las palabras
palabras = []


# Pedir 5 palabras
for i in range(5):
    palabras.append(input(f"Palabra {i + 1}: "))


# Si la cantidad de elementos de la lista es igual
# a la cantidad de elementos del set, no había repetidos.
if len(palabras) == len(set(palabras)):
    print("Todas son distintas")
else:
    print("Hay palabras repetidas")
