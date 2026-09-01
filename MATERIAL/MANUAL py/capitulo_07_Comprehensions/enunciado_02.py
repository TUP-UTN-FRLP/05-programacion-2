# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# ENUNCIADO 2
# Dada la lista [3, 8, -2, 7, -5, 0, 12, -4], generar una lista con
# los valores absolutos (usá abs()).
# -----------------------------------------------------------------------------

numeros = [3, 8, -2, 7, -5, 0, 12, -4]

# -----------------------------------------------------------------------------
# Colección destino: absolutos
# Que tipo de colección destino quiero: lista []
# Cómo guardo los datos: abs(n) (valor absoluto del número)
# Cómo obtengo los datos: n
# Desde que colección: numeros
# Filtrado previo: ninguno
# -----------------------------------------------------------------------------
absolutos = [abs(n) for n in numeros]
print(absolutos)
