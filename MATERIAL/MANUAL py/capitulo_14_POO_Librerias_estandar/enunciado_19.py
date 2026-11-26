# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Uní el capítulo 13 con este: escribí leer_csv(ruta) que devuelva una
# lista de objetos Producto, una dataclass, en vez de diccionarios
# sueltos; y guardar_csv(productos, ruta) que haga lo inverso con
# dataclasses.asdict. Cargá el CSV, filtrá los productos caros y volvé a
# guardarlos. El programa crea primero su propio CSV de ejemplo.
# -------------------------------------------------------------------------

import csv
from dataclasses import asdict, dataclass, fields


@dataclass
class Producto:
    """Producto leído desde una fila de CSV."""

    codigo: str
    nombre: str
    precio: float
    stock: int


def crear_csv_de_ejemplo(ruta):
    """Genera el CSV de entrada con datos de prueba."""
    filas = [
        ("P-001", "Yerba", "3500", "20"),
        ("P-002", "Leche", "800", "15"),
        ("P-003", "Aceite", "4200", "8"),
        ("P-004", "Pan", "950", "40"),
    ]

    with open(ruta, "w", newline="", encoding="utf-8") as salida:
        escritor = csv.writer(salida)
        escritor.writerow([campo.name for campo in fields(Producto)])
        escritor.writerows(filas)


def leer_csv(ruta):
    """Lee el CSV y devuelve una lista de objetos Producto."""
    with open(ruta, newline="", encoding="utf-8") as archivo:
        return [
            Producto(
                codigo=fila["codigo"],
                nombre=fila["nombre"],
                precio=float(fila["precio"]),
                stock=int(fila["stock"]),
            )
            for fila in csv.DictReader(archivo)
        ]


def guardar_csv(productos, ruta):
    """Guarda una lista de Producto en un archivo CSV."""
    if not productos:
        return

    campos = [campo.name for campo in fields(Producto)]

    with open(ruta, "w", newline="", encoding="utf-8") as salida:
        escritor = csv.DictWriter(salida, fieldnames=campos)
        escritor.writeheader()
        escritor.writerows(asdict(p) for p in productos)


if __name__ == "__main__":
    # El CSV devuelve todo como texto: la conversión a float e int
    # es responsabilidad de quien lee.
    crear_csv_de_ejemplo("productos_dc.csv")

    productos = leer_csv("productos_dc.csv")
    caros = [p for p in productos if p.precio > 1000]

    guardar_csv(caros, "productos_caros.csv")

    for producto in caros:
        print(f"  {producto}")

    print(f"Guardados {len(caros)} productos caros")
