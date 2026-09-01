# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# ENUNCIADO 17
# Con el mismo diccionario del ejercicio 16, calculá el valor
# total del inventario (precio × stock, sumados) usando una
# comprensión generadora dentro de sum().
# -----------------------------------------------------------------------------


catalogo = {
    "pan": {"precio": 500, "stock": 20},
    "leche": {"precio": 800, "stock": 5},
    "queso": {"precio": 1200, "stock": 0},
    "yerba": {"precio": 3500, "stock": 15}
}

# -----------------------------------------------------------------------------
# Colección destino: generador (usado dentro de sum())
# Que tipo de colección destino quiero: generador ()
# Cómo guardo los datos: datos["precio"] * datos["stock"] (precio por stock de
# cada producto)
# Cómo obtengo los datos: datos
# Desde que colección: catalogo.values()
# Filtrado previo: ninguno
# -----------------------------------------------------------------------------
total = sum(datos["precio"] * datos["stock"] for datos in catalogo.values())
print(f"Valor total del inventario: ${total}")
