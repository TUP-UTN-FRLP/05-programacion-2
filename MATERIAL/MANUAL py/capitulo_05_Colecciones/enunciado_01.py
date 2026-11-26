# -*- coding: utf-8 -*-
# ---------------------------------------------------------------
# Enunciado 1:
# Dada la lista ["Ana", "Juan", "Pedro", "Ana", "Lucía", "Juan"],
# obtener un set con los nombres sin repetir y mostrar cuántos
# nombres diferentes hay.
#
# PREGUNTA: ¿Y si lo quiero ordenada? ¿Cómo lo haría?
# ---------------------------------------------------------------

# Crear la lista de nombres
nombres = ["Ana", "Juan", "Pedro", "Ana", "Lucía", "Juan"]

# Convertir la lista en un set.
# El set elimina automáticamente los elementos repetidos.
unicos = set(nombres)

# Mostrar la cantidad de nombres únicos y cuáles son
print(f"Hay {len(unicos)} nombres únicos: {unicos}")
