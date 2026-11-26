# ============================================================
# Enunciado 5:
# Pedir números al usuario e ir acumulando su suma.
# Cortar cuando la suma pase de 100 e imprimir cuántos
# números hicieron falta.
# ============================================================

# Inicializar el acumulador de la suma
suma = 0

# Inicializar el contador de números ingresados
cantidad = 0

# Repetir mientras la suma no supere 100
while suma <= 100:

    # Pedir un número
    numero = int(input("Número: "))

    # Acumular el número
    suma += numero

    # Contar cuántos números se ingresaron
    cantidad += 1

# Mostrar la cantidad de números y la suma alcanzada
print(f"Con {cantidad} números la suma llegó a {suma}")
