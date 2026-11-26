# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Ejercicio 2
# Dada la lista [15, 22, 8, 34, 7, 41, 19, 60], obtener una lista
# solo con los números mayores a 20.
# -----------------------------------------------------------------------------

# Colección destino = [expresión - ¿Qué hago con los datos? - for elemento in
# colección - ¿De dónde saco los datos? - ¿Que datos quiero?]
# [todo n de lista numeros si n > 20]
numeros = [15, 22, 8, 34, 7, 41, 19, 60]
grandes = [n for n in numeros if n > 20]
print(grandes)
