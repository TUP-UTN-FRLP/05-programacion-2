# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# ENUNCIADO 6
# Dada la lista [15, 22, 8, 34, 7, 41, 19], generar una lista donde
# cada número esté acompañado por su clasificación:
# [(15, "impar"), (22, "par"), (8, "par"), ...]. Usá una expresión
# condicional ("par" if n % 2 == 0 else "impar").
# -----------------------------------------------------------------------------


numeros = [15, 22, 8, 34, 7, 41, 19]

# -----------------------------------------------------------------------------
# Colección destino: clasificados
# Que tipo de colección destino quiero: lista []
# Cómo guardo los datos: (n, "par" if n % 2 == 0 else "impar")
# (tupla número y clasificación)
# Cómo obtengo los datos: n
# Desde que colección: numeros
# Filtrado previo: ninguno
# -----------------------------------------------------------------------------
clasificados = [(n, "par" if n % 2 == 0 else "impar") for n in numeros]
print(clasificados)
