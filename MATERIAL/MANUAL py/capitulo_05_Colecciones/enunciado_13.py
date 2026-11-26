# -*- coding: utf-8 -*-
# -------------------------------------------------
# Enunciado 13:
# Invertir un diccionario.
# Dado:
# {"a": 1, "b": 2, "c": 3}
# Generar:
# {1: "a", 2: "b", 3: "c"}
# Podés asumir que todos los valores son distintos.
# -------------------------------------------------


# Crear el diccionario original
original = {
    "a": 1,
    "b": 2,
    "c": 3
}
print("Diccionario original:")
print(original)

# Crear un diccionario vacío para guardar el resultado
invertido = {}

# Recorrer las claves y valores del diccionario original
for clave, valor in original.items():

    # Guardar el valor como clave y la clave como valor
    invertido[valor] = clave

# Mostrar el diccionario invertido
print(invertido)
