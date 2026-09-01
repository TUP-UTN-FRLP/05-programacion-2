# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# ENUNCIADO 9
# Dado un texto, generar un diccionario {palabra: longitud} con cada
# palabra única y su cantidad de letras.
# -----------------------------------------------------------------------------


texto = input("Texto: ")

# -----------------------------------------------------------------------------
# Colección destino: longitudes
# Que tipo de colección destino quiero: diccionario {}
# Cómo guardo los datos: palabra: len(palabra) (clave: longitud de la palabra)
# Cómo obtengo los datos: palabra
# Desde que colección: set(texto.lower().split())
# Filtrado previo: ninguno
# -----------------------------------------------------------------------------
longitudes = {palabra: len(palabra) for palabra in set(texto.lower().split())}
print(longitudes)
