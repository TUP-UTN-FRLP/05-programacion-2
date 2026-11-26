# ============================================================
# Enunciado 17:
# Calcular la suma de los múltiplos de 3 o 5 menores a 1000.
# Problema clásico de Project Euler #1.
# ============================================================

# Inicializar el acumulador
suma = 0

# Recorrer los números del 1 al 999
for numero in range(1, 1000):

    # Verificar si es múltiplo de 3 o de 5
    if numero % 3 == 0 or numero % 5 == 0:

        # Acumular el número
        suma += numero

# Mostrar el resultado
print(f"Suma: {suma}")
