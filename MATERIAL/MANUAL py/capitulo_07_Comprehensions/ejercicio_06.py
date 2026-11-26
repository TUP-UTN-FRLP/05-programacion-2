# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Ejercicio 6
# Dada la frase "el perro y el gato y el perro", obtener el set
# de palabras únicas.
#
# PREGUNTA: ¿Por qué solo quedan 4 palabras?
# -----------------------------------------------------------------------------

frase = "el perro y el gato y el perro"

# Colección destino = [expresión - ¿Qué hago con los datos? - for elemento in
# colección - ¿De dónde saco los datos? - ¿Que datos quiero?]
# [toda palabra en lista de palabras de frase generada por split()]
unicas = {palabra for palabra in frase.split()}
print(unicas)
