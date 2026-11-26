# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Guardá una lista de contactos, con nombre y teléfono, en
# contactos.json. Después leelo de vuelta y mostralos por pantalla, para
# comprobar que la ida y la vuelta conservan los datos.
# -------------------------------------------------------------------------

import json


def guardar_contactos(contactos, ruta):
    """Guarda la lista de contactos en un archivo JSON."""
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(contactos, archivo, indent=2, ensure_ascii=False)


def cargar_contactos(ruta):
    """Lee la lista de contactos desde un archivo JSON."""
    with open(ruta, encoding="utf-8") as archivo:
        return json.load(archivo)


if __name__ == "__main__":
    contactos = [
        {"nombre": "Ana Pérez", "telefono": "221-1234"},
        {"nombre": "Juan Gómez", "telefono": "221-5678"},
        {"nombre": "Pedro Díaz", "telefono": "221-9012"},
    ]

    guardar_contactos(contactos, "contactos.json")
    recuperados = cargar_contactos("contactos.json")

    for contacto in recuperados:
        print(f"  {contacto['nombre']}: {contacto['telefono']}")

    assert recuperados == contactos, "Se perdieron datos"
