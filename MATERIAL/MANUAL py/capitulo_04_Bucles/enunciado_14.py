# ============================================================
# Enunciado 14:
# Dada una lista con nombres, imprimir cada nombre
# precedido por su número de orden, empezando en 1.
# ============================================================

# Crear la lista de nombres
nombres = ["Ana", "Juan", "Pedro", "Lucía"]
print(nombres)
nombres = sorted(nombres)  # Ordenar la lista alfabéticamente
print(nombres)
# enumerate() permite obtener el índice y el nombre
# start=1 hace que el índice comience en 1
for indice, nombre in enumerate(nombres, start=1):

    # Mostrar número de orden y nombre
    print(f"{indice}. {nombre}")
