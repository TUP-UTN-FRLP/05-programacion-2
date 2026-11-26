# -*- coding: utf-8 -*-
# -------------------------------------------------------
# Enunciado 11:
# Traductor mini:
# Crear un diccionario con al menos 5 palabras en español
# y su traducción al inglés.
# Pedir una palabra al usuario y devolver la traducción,
# o "No encontrada" si no está.
# Función sugerida: .get()
# -------------------------------------------------------


# Crear el diccionario de traducciones
diccionario = {
    "hola": "hello",
    "gato": "cat",
    "casa": "house",
    "libro": "book",
    "amigo": "friend"
}

# Pedir una palabra y convertirla a minúscula
palabra = input("Palabra en español: ").lower()

# Buscar la palabra.
# Si no existe, .get() devuelve "No encontrada".
traduccion = diccionario.get(palabra, "No encontrada")

# Mostrar el resultado
print(f"Traducción: {traduccion}")
