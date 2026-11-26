# ============================================================
# Enunciado 19:
# Generar los primeros 15 números de la sucesión de Fibonacci.
# Ejemplo: 1, 1, 2, 3, 5, 8, 13, ...
# ============================================================

# Los dos primeros números de la sucesión
a = 1
b = 1

# Mostrar los dos primeros números
print(a, end=" ")
print(b, end=" ")

# Ya mostramos 2 números, por eso faltan 13
for i in range(13):

    # Calcular el siguiente número
    siguiente = a + b

    # Mostrar el siguiente número
    print(siguiente, end=" ")

    # Actualizar los valores para la próxima vuelta
    a = b
    b = siguiente

# Agregar un salto de línea al final
print()
