# ============================================================
# Enunciado 10:
# Dada una lista de números, imprimir solo los positivos,
# y detenerse si encuentra un -99
# (código de "fin de datos").
# ============================================================

# Crear la lista de datos
datos = [5, 3, -2, 8, -99, 10, 7]

# Recorrer todos los números
for numero in datos:

    # Si encontramos -99, terminamos el recorrido
    if numero == -99:
        print("Fin de datos")
        break

    # Si el número es negativo, lo salteamos
    if numero < 0:
        continue

    # Mostrar solamente los números positivos
    print(numero)
