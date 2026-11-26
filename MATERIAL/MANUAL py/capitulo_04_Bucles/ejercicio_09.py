# ============================================================
# Enunciado 9:
# Tenés dos listas paralelas, una con productos y otra
# con precios.
#
# Imprimir el catálogo y calcular el total.
# ============================================================

# Lista de productos
productos = ["pan", "leche", "queso", "yerba"]

# Lista de precios correspondiente a cada producto
precios = [500, 800, 1200, 3500]

# Inicializar el acumulador
total = 0

# Recorrer las dos listas en paralelo
for producto, precio in zip(productos, precios):

    # Mostrar producto y precio
    print(f"{producto}: ${precio}")

    # Acumular el precio
    total += precio

# Mostrar el total del catálogo
print(f"Total del catálogo: ${total}")
