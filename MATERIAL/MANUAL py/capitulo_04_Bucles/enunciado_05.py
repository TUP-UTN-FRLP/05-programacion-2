# ============================================================
# Enunciado 5:
# Dada la lista [7, 3, 9, 1, 8, 4], mostrar el mayor
# y el menor sin usar max() ni min().
# ============================================================


lista = [7, 3, 9, 1, 8, 4]


# Suponemos inicialmente que el primer elemento
# es tanto el mayor como el menor
mayor = lista[0]
menor = lista[0]

# Recorrer todos los elementos de la lista
for numero in lista:

    # Si encontramos un número mayor, lo guardamos
    if numero > mayor:
        mayor = numero

    # Si encontramos un número menor, lo guardamos
    if numero < menor:
        menor = numero

# Mostrar los resultados
print(f"Mayor: {mayor}, Menor: {menor}")
