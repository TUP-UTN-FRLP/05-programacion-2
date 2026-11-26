# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# ENUNCIADO 1
# Generar una lista con los primeros 20 múltiplos de 5
# (5, 10, 15, ..., 100).
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Colección destino = [¿Qué hago con los datos? - for variable que guarda
# elemento in colección de origen - Filtro de los datos (opcional)]
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Colección destino: multiplos
# Que tipo de colección destino quiero: lista []
# Cómo guardo los datos: n * 5 (múltiplo de 5)
# Cómo obtengo los datos: n
# Desde que colección: range(1, 21)
# Filtrado previo: ninguno
# -----------------------------------------------------------------------------
multiplos = [n * 5 for n in range(1, 21)]
print(multiplos)
