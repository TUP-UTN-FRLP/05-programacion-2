# ============================================================
# Enunciado 9:
# Dada la lista [15, 22, 8, 34, 7, 41, 19],
# imprimir solamente los números pares.
# ============================================================


lista = [15, 22, 8, 34, 7, 41, 19]


# Recorrer todos los números
for numero in lista:

    # Un número es par si el resto de dividirlo por 2 es 0
    if numero % 2 == 0:
        print(numero, end=" ")
