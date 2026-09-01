# ============================================================
# Enunciado 12:
# Dada la tupla ("Ana", "Juan", "Pedro", "Lucía")
# y la lista [8, 6, 9, 7], mostrar cada nombre con su nota.
# ============================================================

# Crear la tupla de nombres
nombres = ("Ana", "Juan", "Pedro", "Lucía")

# Crear la lista de notas
notas = [8, 6, 9, 7]

# Recorrer ambas colecciones en paralelo
for nombre, nota in zip(nombres, notas):

    # Mostrar cada nombre junto con su nota
    print(f"{nombre}: {nota}")
