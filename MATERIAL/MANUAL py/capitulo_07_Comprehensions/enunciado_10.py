# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# ENUNCIADO 10
# Invertí este diccionario: {"a": 1, "b": 2, "c": 3}
# -> {1: "a", 2: "b", 3: "c"}.
# -----------------------------------------------------------------------------


original = {"a": 1, "b": 2, "c": 3}

# -----------------------------------------------------------------------------
# Colección destino: invertido
# Que tipo de colección destino quiero: diccionario {}
# Cómo guardo los datos: v: k (valor original como nueva clave, clave original
# como nuevo valor)
# Cómo obtengo los datos: k, v (desempaquetado de cada tupla)
# Desde que colección: original.items()
# Filtrado previo: ninguno
# -----------------------------------------------------------------------------
invertido = {v: k for k, v in original.items()}
print(invertido)
