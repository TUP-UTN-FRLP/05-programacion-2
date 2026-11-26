# -*- coding: utf-8 -*-
# ----------------------------------------------
# Enunciado 19:
# Dados dos diccionarios de precios:
# precios_marzo = {"pan": 500, "leche": 800}
# precios_abril = {
# "pan": 550,
# "leche": 850,
# "queso": 1200
# }
# Mostrar el aumento porcentual de cada producto
# que exista en ambos diccionarios.
# ----------------------------------------------

# Precios del mes de marzo
precios_marzo = {
    "pan": 500,
    "leche": 800
}

# Precios del mes de abril
precios_abril = {
    "pan": 550,
    "leche": 850,
    "queso": 1200
}

# Recorrer los productos de marzo
for producto in precios_marzo:

    # Comprobar si también existe en abril
    if producto in precios_abril:

        # Obtener el precio anterior
        viejo = precios_marzo[producto]

        # Obtener el precio nuevo
        nuevo = precios_abril[producto]

        # Calcular el aumento porcentual
        aumento = (nuevo - viejo) / viejo * 100

        # Mostrar el aumento
        print(f"{producto}: {aumento:.2f}%")
