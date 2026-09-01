# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# ENUNCIADO 5
# Dado un string, generar una lista con las posiciones en las
# que aparece la letra "a" (usá enumerate()).
# -----------------------------------------------------------------------------


texto = input("Texto: ")

# -----------------------------------------------------------------------------
# Colección destino: posiciones
# Que tipo de colección destino quiero: lista []
# Cómo guardo los datos: i (el índice sin modificar)
# Cómo obtengo los datos: i, letra (desempaquetado de cada tupla)
# Desde que colección: enumerate(texto.lower())
# Filtrado previo: letra == "a" (solo posiciones donde aparece la "a")
# -----------------------------------------------------------------------------
posiciones = [i for i, letra in enumerate(texto.lower()) if letra == "a"]
print(f"La 'a' aparece en las posiciones: {posiciones}")
