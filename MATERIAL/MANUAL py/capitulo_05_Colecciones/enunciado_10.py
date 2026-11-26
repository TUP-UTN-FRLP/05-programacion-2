# -*- coding: utf-8 -*-
# -------------------------------------------------------------
# Enunciado 10:
# Dada una lista de compras:
# [("pan", 500), ("leche", 800), ("pan", 500), ("queso", 1200)]
# Armar un diccionario que agrupe la cantidad de veces
# que aparece cada producto.
# Resultado esperado:
# {"pan": 2, "leche": 1, "queso": 1}
# -------------------------------------------------------------

# Crear la lista de compras
compras = [
    ("pan", 500),
    ("leche", 800),
    ("pan", 500),
    ("queso", 1200)
]

# Crear un diccionario vacío para contar las apariciones
cantidades = {}

# Recorrer la lista y desempaquetar cada tupla
for producto, precio in compras:

    # Obtener la cantidad actual o 0 si es la primera aparición
    cantidades[producto] = cantidades.get(producto, 0) + 1

# Mostrar las cantidades
print(cantidades)
