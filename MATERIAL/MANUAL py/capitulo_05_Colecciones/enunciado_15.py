# -*- coding: utf-8 -*-
# --------------------------------------------------------
# Enunciado 15:
# Dada una frase, devolver un set con las palabras únicas,
# sin repetidos y todo en minúscula.
# Funciones sugeridas:
# .split(), set(), .lower()
# --------------------------------------------------------


# Pedir una frase
frase = input("Frase: ")

# Convertir a minúscula, separar en palabras
# y eliminar los repetidos mediante set()
palabras_unicas = set(frase.lower().split())

# Mostrar las palabras únicas
print(f"Palabras únicas ({len(palabras_unicas)}): {palabras_unicas}")
