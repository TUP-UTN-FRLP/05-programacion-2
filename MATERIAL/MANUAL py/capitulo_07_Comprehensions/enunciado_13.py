# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# ENUNCIADO 13
# Dada la lista [7, 3, 3, 5, 9, 7, 2, 5, 9, 9], obtené el set
# de los números que se repiten (aparecen más de una vez).
# Pista: podés usar .count().
# -----------------------------------------------------------------------------


numeros = [7, 3, 3, 5, 9, 7, 2, 5, 9, 9]

# -----------------------------------------------------------------------------
# Colección destino: repetidos
# Que tipo de colección destino quiero: set {}
# Cómo guardo los datos: n (el número sin modificar)
# Cómo obtengo los datos: n
# Desde que colección: numeros
# Filtrado previo: numeros.count(n) > 1 (números que aparecen más de una vez)
# -----------------------------------------------------------------------------
repetidos = {n for n in numeros if numeros.count(n) > 1}
print(repetidos)
