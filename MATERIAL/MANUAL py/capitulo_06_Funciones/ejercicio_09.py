# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Tenés esta lista de productos como tuplas (nombre, precio, stock).
# Ordenala primero por precio, después por stock (de menor a mayor),
# y encontrá el producto más caro.
# -------------------------------------------------------------------


productos = [
    ("pan", 500, 20),
    ("leche", 800, 5),
    ("queso", 1200, 3),
    ("yerba", 3500, 15)
]

por_precio = sorted(productos, key=lambda p: p[1])
por_stock = sorted(productos, key=lambda p: p[2])
mas_caro = max(productos, key=lambda p: p[1])

print(f"Por precio: {por_precio}")
print(f"Por stock: {por_stock}")
print(f"Más caro: {mas_caro}")
