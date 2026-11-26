# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# ENUNCIADO 12
# Dada una lista de palabras, obtené el set de las que empiezan
# con vocal.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Colección destino: con_vocal
# Que tipo de colección destino quiero: set {}
# Cómo guardo los datos: p (la palabra sin modificar)
# Cómo obtengo los datos: p
# Desde que colección: palabras
# Filtrado previo: p[0].lower() in "aeiouáéíóú" (palabras que empiezan
# con vocal)
# -----------------------------------------------------------------------------
palabras = ["mesa", "árbol", "sol", "escuela", "isla", "banana", "uva"]
con_vocal = {p for p in palabras if p[0].lower() in "aeiouáéíóú"}
print(con_vocal)
