# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# ENUNCIADO 15
# Con la misma lista de precios, contá cuántos superan los 1000
# usando sum() con una comprensión generadora que devuelva
# booleanos. (Truco pythónico: True == 1, False == 0.)
# -----------------------------------------------------------------------------


precios = [500, 1200, 800, 1500, 950, 2000, 3500]

# -----------------------------------------------------------------------------
# Colección destino: generador (usado dentro de sum())
# Que tipo de colección destino quiero: generador ()
# Cómo guardo los datos: p > 1000 (True si el precio supera $1000, False si no)
# Cómo obtengo los datos: p
# Desde que colección: precios
# Filtrado previo: ninguno
# -----------------------------------------------------------------------------
caros = sum(p > 1000 for p in precios)

print(f"Precios sobre $1000: {caros}")
