# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# ENUNCIADO 18
# Dada la matriz [[1, 2, 3], [4, 5, 6], [7, 8, 9]], obtené una
# lista aplanada con todos los elementos. Se permite comprensión
# anidada.
# -----------------------------------------------------------------------------


matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# -----------------------------------------------------------------------------
# Colección destino: aplanada
# Que tipo de colección destino quiero: lista []
# Cómo guardo los datos: x (el elemento sin modificar)
# Cómo obtengo los datos: x (de cada fila), fila (de la matriz)
# Desde que colección: matriz (lista de listas anidadas)
# Filtrado previo: ninguno
# -----------------------------------------------------------------------------
aplanada = [x for fila in matriz for x in fila]
print(aplanada)
