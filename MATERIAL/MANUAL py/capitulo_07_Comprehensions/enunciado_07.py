# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# ENUNCIADO 7
# Dada la lista de nombres ["Ana", "Juan", "Sofía", "Pedro",
# "Lucía"] y la lista de notas [8, 6, 9, 5, 7], generar una
# lista de strings tipo "Ana: 8" usando zip().
# -----------------------------------------------------------------------------


nombres = ["Ana", "Juan", "Sofía", "Pedro", "Lucía"]
notas = [8, 6, 9, 5, 7]

# -----------------------------------------------------------------------------
# Colección destino: reporte
# Que tipo de colección destino quiero: lista []
# Cómo guardo los datos: f"{n}: {nota}" (string formateado con nombre y nota)
# Cómo obtengo los datos: n, nota (desempaquetado de cada tupla)
# Desde que colección: zip(nombres, notas)
# Filtrado previo: ninguno
# -----------------------------------------------------------------------------
reporte = [f"{n}: {nota}" for n, nota in zip(nombres, notas)]
print(reporte)
