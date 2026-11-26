# ============================================================
# Enunciado 3:
# Dada la lista ["Ana", "Juan", "Pedro", "Lucía", "Diego"],
# reemplazar los dos del medio (Pedro y Lucía) por
# ["Sofía", "Martín", "Camila"].
#
# Después, borrar los dos primeros usando asignación
# de slicing.
# ============================================================

# Crear la lista de alumnos
alumnos = ["Ana", "Juan", "Pedro", "Lucía", "Diego"]
print(alumnos)
print()
# Reemplazar Pedro y Lucía por tres nuevos elementos
# [2:4] toma las posiciones 2 y 3
alumnos[2:4] = ["Sofía", "Martín", "Camila"]

# Mostrar la lista después del reemplazo
print(alumnos)
print()

# Borrar los dos primeros elementos
# Asignar una lista vacía elimina ese tramo
alumnos[:2] = []

# Mostrar la lista resultante
print(alumnos)
