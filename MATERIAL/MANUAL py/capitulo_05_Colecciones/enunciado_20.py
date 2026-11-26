# -*- coding: utf-8 -*-
# ------------------------------------------
# Enunciado 20:
# Dado un diccionario con productos y stock:
# stock = {
# "pan": 20,
# "leche": 5,
# "queso": 0,
# "yogur": 15
# }
# Generar tres listas:
# - Productos disponibles (stock > 5)
# - Con poco stock (entre 1 y 5)
# - Agotados (stock = 0)
# ------------------------------------------

# Crear el diccionario de productos y stock
stock = {
    "pan": 20,
    "leche": 5,
    "queso": 0,
    "yogur": 15,
    "manteca": 3
}

# Crear las tres listas de clasificación
disponibles = []
pocos = []
agotados = []

# Recorrer productos y cantidades
for producto, cantidad in stock.items():

    # Stock igual a cero
    if cantidad == 0:
        agotados.append(producto)

    # Stock entre 1 y 5
    elif cantidad <= 5:
        pocos.append(producto)

    # Stock mayor que 5
    else:
        disponibles.append(producto)

# Mostrar las tres categorías
print(f"Disponibles: {disponibles}")
print(f"Poco stock: {pocos}")
print(f"Agotados: {agotados}")
