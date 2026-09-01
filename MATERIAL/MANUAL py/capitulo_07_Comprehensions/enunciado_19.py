# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# ENUNCIADO 19
# Con la misma matriz, obtené una lista solo con los números pares.
# -----------------------------------------------------------------------------


matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# -----------------------------------------------------------------------------
# Colección destino: pares
# Que tipo de colección destino quiero: lista []
# Cómo guardo los datos: x (el número sin modificar)
# Cómo obtengo los datos: x (de cada fila), fila (de la matriz)
# Desde que colección: matriz (lista de listas anidadas)
# Filtrado previo: x % 2 == 0 (solo números pares)
# -----------------------------------------------------------------------------
pares = [x for fila in matriz for x in fila if x % 2 == 0]
print(pares)
