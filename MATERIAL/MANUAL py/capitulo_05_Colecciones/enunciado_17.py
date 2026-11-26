# -*- coding: utf-8 -*-
# -------------------------------------------------------
# Enunciado 17:
# Dado un texto, contar cuántas palabras aparecen y armar
# un diccionario con la frecuencia de cada una.
# Mostrar las 3 palabras más frecuentes.
# Funciones sugeridas:
# .split()
# sorted() con key
# -------------------------------------------------------

# Pedir un texto y convertirlo a minúscula
texto = input("Texto: ").lower()

# Separar el texto en palabras
palabras = texto.split()

# Crear un diccionario para contar frecuencias
frecuencia = {}

# Recorrer cada palabra
for palabra in palabras:

    # Incrementar el contador de la palabra
    frecuencia[palabra] = frecuencia.get(palabra, 0) + 1

# Mostrar la cantidad total de palabras
print(f"Cantidad total de palabras: {len(palabras)}")

# Mostrar la cantidad de palabras diferentes
print(f"Palabras distintas: {len(frecuencia)}")

# Ordenar por frecuencia de mayor a menor
# par[1] representa la cantidad de veces que aparece
top_3 = sorted(
    frecuencia.items(),
    key=lambda par: par[1],
    reverse=True
)[:3]

# Mostrar las tres palabras más frecuentes
print("Las 3 más frecuentes:")

for palabra, veces in top_3:
    print(f"  {palabra}: {veces}")
