# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# Enunciado 4:
# Creá un diccionario con datos de un producto
# (nombre, precio, stock).
# Después:
# - subile el precio un 10%,
# - agregale una clave "categoría",
# - consultá si tiene "descuento"
# sin que rompa si no está.
#
# PREGUNTA: ¿Porque la salida de precio es 3850.0000000000005
#           si matemáticamente es 3850?
#
# PREGUNTA: Revisando la impresión, ¿Como mejorarías
#           la salida para que sea más clara y entendible?
# -----------------------------------------------------------

# Crear el diccionario del producto
producto = {
    "nombre": "Yerba",
    "precio": 3500,
    "stock": 15
}

# Aumentar el precio un 10%
producto["precio"] = producto["precio"] * 1.10

# Agregar una nueva clave
producto["categoria"] = "Almacén"

# Consultar el descuento.
# Si la clave no existe, devolver 0.
descuento = producto.get("descuento", 0)

# Mostrar el producto
print(producto)

# Mostrar el descuento
print(f"Descuento actual: {descuento}%")
