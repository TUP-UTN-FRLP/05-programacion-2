# ============================================================
# Enunciado 16:
# Dada una lista de precios, aplicar 15% de descuento
# a los que superan $1000 y dejar los demás sin cambios.
# Mostrar la lista modificada.
#
# NOTA: Prestar atención en como mostramos los datos
# ============================================================


# Crear la lista de precios
precios = [500, 1200, 800, 1500, 950, 2000]
print("Precios originales:")
print([f"{p:.2f}" for p in precios])
print()

# Recorrer la lista mediante sus índices
for i in range(len(precios)):

    # Aplicar descuento solamente a precios mayores a 1000
    if precios[i] > 1000:
        precios[i] = precios[i] * 0.85

# Mostrar la lista modificada
print("Precios con descuento aplicado:")
print([f"{p:.2f}" for p in precios])
