# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# ENUNCIADO 8
# Dado el diccionario {"pan": 500, "leche": 800, "queso": 1200,
# "yerba": 3000}, generar un diccionario nuevo con los precios en
# dólares (dividir por 1000 y redondear a 2 decimales).
# -----------------------------------------------------------------------------


precios = {"pan": 500, "leche": 800, "queso": 1200, "yerba": 3000}

# -----------------------------------------------------------------------------
# Colección destino: en_dolares
# Que tipo de colección destino quiero: diccionario {}
# Cómo guardo los datos: producto: round(precio / 1000, 2)
# (clave: precio redondeado en dólares)
# Cómo obtengo los datos: producto, precio (desempaquetado de cada tupla)
# Desde que colección: precios.items()
# Filtrado previo: ninguno
# -----------------------------------------------------------------------------
en_dolares = {
    producto: round(precio / 1000, 2)
    for producto, precio in precios.items()
}
print(en_dolares)
