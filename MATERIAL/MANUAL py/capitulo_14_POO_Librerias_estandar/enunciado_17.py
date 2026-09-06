# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Escribí generar_reporte_diario() que arme un reporte con un timestamp,
# elija 5 productos al azar con random.sample y lo guarde como JSON en
# reportes/reporte_AAAAMMDD.json, creando la carpeta con pathlib.
# Cuidado con un detalle: pedí la hora UNA sola vez y reutilizá ese
# valor. Si llamás datetime.now() dos veces, un programa que cruce la
# medianoche entre ambas llamadas guarda una fecha inconsistente.
# -------------------------------------------------------------------------

import json
import random
from datetime import datetime
from pathlib import Path

PRODUCTOS = [
    "Pan",
    "Leche",
    "Yerba",
    "Café",
    "Fideos",
    "Arroz",
    "Azúcar",
    "Aceite",
]


def generar_reporte_diario(carpeta=Path("reportes")):
    """Genera un reporte diario en JSON y devuelve su ruta."""
    momento = datetime.now()

    reporte = {
        "generado_en": momento.isoformat(timespec="seconds"),
        "productos_destacados": random.sample(PRODUCTOS, 5),
    }

    carpeta.mkdir(parents=True, exist_ok=True)
    ruta = carpeta / f"reporte_{momento:%Y%m%d}.json"

    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(reporte, archivo, indent=2, ensure_ascii=False)

    return ruta


if __name__ == "__main__":
    # f"{momento:%Y%m%d}" es equivalente a momento.strftime("%Y%m%d"):
    # las f-strings aceptan directamente el formato de strftime.
    random.seed(7)

    ruta = generar_reporte_diario()
    print(f"Reporte guardado en: {ruta}")
    print(ruta.read_text(encoding="utf-8"))
