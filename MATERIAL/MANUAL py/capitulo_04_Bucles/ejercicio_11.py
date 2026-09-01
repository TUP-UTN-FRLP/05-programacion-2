# ============================================================
# Enunciado 11:
# Dada la lista de notas:
# [7, 4, 9, 6, 8, 3, 10, 5]
#
# Mostrar:
# - La cantidad
# - El promedio
# - La nota más alta
# - La nota más baja
#
# Después, ordenarla de mayor a menor sin modificar
# la lista original.
# ============================================================

# Crear la lista de notas
notas = [7, 4, 9, 6, 8, 3, 10, 5]

# Mostrar la cantidad de notas
print(f"Cantidad: {len(notas)}")

# Calcular y mostrar el promedio
print(f"Promedio: {sum(notas) / len(notas):.2f}")

# Mostrar la nota mayor y la menor
print(f"Mayor: {max(notas)}, Menor: {min(notas)}")

# Crear una nueva lista ordenada de mayor a menor
# reverse=True invierte el orden
ordenadas = sorted(notas, reverse=True)

# Mostrar la lista ordenada
print(f"Ordenadas: {ordenadas}")

# Comprobar que la lista original no fue modificada
print(f"Original sin tocar: {notas}")
