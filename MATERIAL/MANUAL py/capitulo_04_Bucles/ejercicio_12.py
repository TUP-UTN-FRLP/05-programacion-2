# ============================================================
# Enunciado 12:
# Buscar si un número dado está en una lista y avisar
# si lo encontraste o no, usando for...else.
# ============================================================

# Crear la lista
lista = [3, 7, 12, 5, 8, 15]

# Pedir el número que queremos buscar
buscado = int(input("¿Qué número buscás?: "))

# Recorrer la lista
for numero in lista:

    # Comprobar si encontramos el número buscado
    if numero == buscado:
        print("Encontrado en la lista")
        break

# El else pertenece al FOR, no al IF.
# Se ejecuta solamente si el for termina sin ejecutar break.
else:
    print(f"{buscado} no está en la lista")
