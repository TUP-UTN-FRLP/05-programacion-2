# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Integrador: leé un CSV de transacciones con fecha, tipo y monto;
# parseá las fechas con datetime.strptime; agrupá por mes con
# defaultdict; contá las transacciones y sumá el total de cada mes; y
# guardá el resultado en JSON con formato
# {"AAAA-MM": {"cantidad": N, "total": X}}. El programa crea primero su
# propio CSV de ejemplo para poder correrse tal cual.
# -------------------------------------------------------------------------

import csv
import json
from collections import defaultdict
from datetime import datetime

FORMATO_FECHA = "%Y-%m-%d"


def crear_csv_de_ejemplo(ruta):
    """Genera el CSV de transacciones con datos de prueba."""
    filas = [
        ("2026-01-05", "deposito", "15000.00"),
        ("2026-01-18", "extraccion", "4000.00"),
        ("2026-02-02", "deposito", "22000.50"),
        ("2026-02-14", "deposito", "8000.00"),
        ("2026-02-27", "extraccion", "3500.25"),
        ("2026-03-09", "deposito", "12000.00"),
    ]

    with open(ruta, "w", newline="", encoding="utf-8") as salida:
        escritor = csv.writer(salida)
        escritor.writerow(["fecha", "tipo", "monto"])
        escritor.writerows(filas)


def resumir_por_mes(ruta):
    """Agrupa las transacciones por mes y devuelve el resumen."""
    resumen = defaultdict(lambda: {"cantidad": 0, "total": 0.0})

    with open(ruta, newline="", encoding="utf-8") as archivo:
        for fila in csv.DictReader(archivo):
            fecha = datetime.strptime(
                fila["fecha"], FORMATO_FECHA
            )
            clave = f"{fecha:%Y-%m}"

            resumen[clave]["cantidad"] += 1
            resumen[clave]["total"] += float(fila["monto"])

    return dict(resumen)


def guardar_json(resumen, ruta):
    """Guarda el resumen mensual en un archivo JSON."""
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(resumen, archivo, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    crear_csv_de_ejemplo("transacciones.csv")

    resumen = resumir_por_mes("transacciones.csv")
    guardar_json(resumen, "resumen_mensual.json")

    for mes in sorted(resumen):
        datos = resumen[mes]
        print(
            f"  {mes}: {datos['cantidad']} transacciones, "
            f"${datos['total']:,.2f}"
        )
