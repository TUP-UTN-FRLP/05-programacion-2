# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# ENUNCIADO 3
# Convertí la lista ["hola", "mundo", "python"] a una lista con
# todas las palabras en mayúsculas.
# -----------------------------------------------------------------------------


palabras = ["hola", "mundo", "python"]

# -----------------------------------------------------------------------------
# Colección destino: mayus
# Que tipo de colección destino quiero: lista []
# Cómo guardo los datos: p.upper() (palabra en mayúsculas)
# Cómo obtengo los datos: p
# Desde que colección: palabras
# Filtrado previo: ninguna
# -----------------------------------------------------------------------------
mayus = [p.upper() for p in palabras]
print(mayus)
