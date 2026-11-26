# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Escribí un programa que lea un CSV de productos con codigo, nombre,
# precio y stock, y genere otro CSV con un 15% de descuento aplicado a
# los precios. El programa debe ser autocontenido: primero crea el CSV
# de entrada con datos de ejemplo y después lo procesa, así se puede
# ejecutar tal cual sin preparar archivos a mano.
# -------------------------------------------------------------------------

import csv

CAMPOS = ["codigo", "nombre", "precio", "stock"]


def crear_csv_de_ejemplo(ruta):
    """Genera el CSV de entrada con datos de prueba."""
    productos = [
        {
            "codigo": "P-001",
            "nombre": "Yerba",
            "precio": "3500.00",
            "stock": "20",
        },
        {
            "codigo": "P-002",
            "nombre": "Leche",
            "precio": "800.00",
            "stock": "15",
        },
        {
            "codigo": "P-003",
            "nombre": "Aceite",
            "precio": "4200.00",
            "stock": "8",
        },
    ]

    with open(ruta, "w", newline="", encoding="utf-8") as salida:
        escritor = csv.DictWriter(salida, fieldnames=CAMPOS)
        escritor.writeheader()
        escritor.writerows(productos)


def aplicar_descuento(ruta_entrada, ruta_salida, porcentaje):
    """Copia el CSV aplicando un descuento a la columna precio."""
    with open(
        ruta_entrada, newline="", encoding="utf-8"
    ) as entrada:
        productos = list(csv.DictReader(entrada))

    factor = 1 - porcentaje / 100

    for producto in productos:
        precio = float(producto["precio"])
        producto["precio"] = f"{precio * factor:.2f}"

    with open(
        ruta_salida, "w", newline="", encoding="utf-8"
    ) as salida:
        escritor = csv.DictWriter(salida, fieldnames=CAMPOS)
        escritor.writeheader()
        escritor.writerows(productos)

    return productos


if __name__ == "__main__":
    # newline="" evita las líneas en blanco extra en Windows.
    crear_csv_de_ejemplo("productos.csv")

    rebajados = aplicar_descuento(
        "productos.csv", "productos_descuento.csv", 15
    )

    for producto in rebajados:
        print(f"  {producto['nombre']}: ${producto['precio']}")
