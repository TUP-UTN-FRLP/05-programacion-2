# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# Enunciado 5:
# Pedir al usuario un producto y su precio, hasta que ingrese
# "fin".
# Guardar todo en un diccionario {producto: precio}
# e imprimirlo al final.
#
# NOTA: En proximos capítulo veremos como validar la entrada
#       del precio y repetir hasta que sea un número válido.
#       Intentalo con lo que ya sabemos.
# -----------------------------------------------------------

# Crear un diccionario vacío para almacenar los productos
productos = {}

# Pedir el primer producto
producto = input("Producto (o 'fin'): ")

# Repetir mientras el usuario no ingrese "fin"
while producto.lower() != "fin":

    # Pedir el precio del producto
    precio = float(input(f"Precio de {producto}: "))

    # Guardar producto y precio en el diccionario
    productos[producto] = precio

    # Pedir el siguiente producto
    producto = input("Producto (o 'fin'): ")

# Mostrar la lista de productos
print("\nLista de productos:")

# Recorrer el diccionario mostrando producto y precio
for nombre, precio in productos.items():
    print(f"  {nombre}: ${precio:.2f}")
