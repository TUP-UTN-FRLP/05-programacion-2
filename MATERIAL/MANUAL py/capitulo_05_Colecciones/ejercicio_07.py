# -*- coding: utf-8 -*-
# -------------------------------------------------------------
# Enunciado 7:
# Dada la lista ["Ana", "Juan", "Ana", "Pedro", "Juan", "Ana"],
# obtener una lista con los nombres únicos,
# ordenados alfabéticamente.
# -------------------------------------------------------------

# Crear la lista original
nombres = ["Ana", "Juan", "Ana", "Pedro", "Juan", "Ana"]

# Convertir a set para eliminar duplicados
# y luego ordenar alfabéticamente.
unicos = sorted(set(nombres))

# Mostrar la lista resultante
print(unicos)
