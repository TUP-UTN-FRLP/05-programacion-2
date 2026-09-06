# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Escribí guardar_y_recuperar(objeto, ruta) que reciba un objeto Python,
# dict o lista, lo guarde en JSON en la ruta indicada, lo vuelva a leer y
# verifique con assert que el resultado es igual al original. Probá qué
# pasa con una tupla y explicá el resultado.
# -------------------------------------------------------------------------

import json
from pathlib import Path


def guardar_y_recuperar(objeto, ruta):
    """Guarda un objeto en JSON y verifica la ida y vuelta."""
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(objeto, archivo, indent=2, ensure_ascii=False)

    with open(ruta, encoding="utf-8") as archivo:
        recuperado = json.load(archivo)

    assert recuperado == objeto, (
        "El objeto cambió después de la ida y vuelta"
    )

    return recuperado


if __name__ == "__main__":
    datos = {
        "nombre": "Ana Pérez",
        "notas": [7, 8, 9],
        "aprobada": True,
        "observacion": None,
    }

    print(guardar_y_recuperar(datos, "prueba.json"))

    # ensure_ascii=False guarda "Pérez" tal cual; con el valor por
    # defecto quedaría escrito como "P\u00e9rez".
    print(Path("prueba.json").read_text(encoding="utf-8"))

    # JSON no tiene tuplas: se serializan como listas y vuelven
    # como listas. Por eso este assert falla.
    try:
        guardar_y_recuperar({"punto": (3, 5)}, "tupla.json")
    except AssertionError as error:
        print(f"Esperado: {error}")
