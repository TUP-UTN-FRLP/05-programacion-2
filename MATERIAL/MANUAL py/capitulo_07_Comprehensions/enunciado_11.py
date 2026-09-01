# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# ENUNCIADO 11
# Dado el diccionario {"Ana": 8, "Juan": 5, "Pedro": 9,
# "Lucía": 4, "Diego": 7}, generar otro diccionario que
# contenga solo los aprobados (nota >= 7).
# -----------------------------------------------------------------------------


notas = {"Ana": 8, "Juan": 5, "Pedro": 9, "Lucía": 4, "Diego": 7}


# -----------------------------------------------------------------------------
# Colección destino: aprobados
# Que tipo de colección destino quiero: diccionario {}
# Cómo guardo los datos: nombre: nota (clave: nota sin modificar)
# Cómo obtengo los datos: nombre, nota (desempaquetado de cada tupla)
# Desde que colección: notas.items()
# Filtrado previo: nota >= 7 (solo aprobados)
# -----------------------------------------------------------------------------
aprobados = {nombre: nota for nombre, nota in notas.items() if nota >= 7}
print(aprobados)
