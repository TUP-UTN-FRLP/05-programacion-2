# -*- coding: utf-8 -*-
# ---------------------------------------------------------
# Enunciado 5:
# Dado un diccionario de stock, pedirle al usuario
# un producto y su cantidad, y "vender" (restar del stock).
# Si al terminar la venta el stock llega a 0,
# eliminar el producto del diccionario.
# ---------------------------------------------------------

# Crear el diccionario de stock
stock = {
    "pan": 20,
    "leche": 5,
    "yerba": 10
}

# Pedir el producto que se quiere vender
producto = input("¿Qué producto vendés?: ")

# Comprobar si el producto existe en el stock
if producto in stock:

    # Pedir la cantidad a vender
    mensaje = "¿Cuántas unidades?: "
    cantidad = input(mensaje)

    # Validad cantidad ingresada
    while not cantidad.isdigit():
        print("Cantidad inválida")
        print("Ingrese un número entero positivo")
        cantidad = input(mensaje)

    cantidad = int(cantidad)

    # Restar la cantidad vendida del stock
    stock[producto] -= cantidad

    # Si el stock llega a cero o queda por debajo,
    # eliminar el producto
    if stock[producto] <= 0:
        del stock[producto]
        print(f"Se agotó {producto}")

    # Mostrar el stock actualizado
    print(stock)

else:
    print("No tenemos ese producto")
