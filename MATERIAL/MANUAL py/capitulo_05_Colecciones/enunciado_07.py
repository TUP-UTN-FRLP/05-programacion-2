# -*- coding: utf-8 -*-
# ------------------------------------------------------
# Enunciado 7:
# Contar cuántas veces aparece cada letra en una palabra
# ingresada por el usuario.
# Ejemplo:
# "banana" -> {"b": 1, "a": 3, "n": 2}
# ------------------------------------------------------


# Pedir una palabra y convertirla a minúscula
palabra = input("Palabra: ").lower()


# Crear un diccionario vacío para guardar los conteos
conteo = {}


# Recorrer cada letra de la palabra
for letra in palabra:

    # Si la letra ya está en el diccionario,
    # incrementar su contador
    if letra in conteo:
        conteo[letra] += 1

    # Si aparece por primera vez, comenzar el contador en 1
    else:
        conteo[letra] = 1

# Mostrar el resultado
print(conteo)
