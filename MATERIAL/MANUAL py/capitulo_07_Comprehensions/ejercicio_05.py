# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Ejercicio 5
# Dada la lista ["Ana", "Juan", "Pedro", "Lucía"], genera un
# diccionario donde la clave sea el nombre y el valor su longitud.
# -----------------------------------------------------------------------------

nombres = ["Ana", "Juan", "Pedro", "Lucía"]

# Colección destino = [expresión - ¿Qué hago con los datos? - for elemento in
# colección - ¿De dónde saco los datos?]
# Es un diccionario con clave:valor, donde la clave es el nombre y el valor
# es la longitud del nombre. Por eso usamos llaves {} en lugar de corchetes [].
# [por cada nombre guarda, nombre:largo por cada nombre de nombres]
longitudes = {len(n): n for n in nombres}
print(longitudes)
