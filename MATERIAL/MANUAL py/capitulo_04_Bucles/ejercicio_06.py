# ============================================================
# Enunciado 6:
# Dada la lista:
# precios = [1500, 2300, 800, 4200, 1900]
#
# Calcular el total a pagar y el precio promedio.
# ============================================================

# Crear la lista de precios
precios = [1500, 2300, 800, 4200, 1900]

# Inicializar el acumulador
total = 0

# Recorrer todos los precios
for precio in precios:

    # Acumular cada precio
    total += precio

# Calcular el promedio
promedio = total / len(precios)

# Mostrar el total y el promedio
print(f"Total: ${total}, Promedio: ${promedio:.2f}")
