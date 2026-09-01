# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Enunciado 20:
# Escribí una función crear_ficha(nombre, edad, datos_extra)
# que devuelva un diccionario con al menos las claves
# "nombre" y "edad", más cualquier dato extra que se le pase
# por nombre.
#
# Pista: **kwargs en la definición recibe todos los argumentos
# por nombre como diccionario.
#
# Ejemplo:
# crear_ficha("Ana", 25, carrera="TUP", ciudad="La Plata")
# debe devolver:
# {"nombre": "Ana", "edad": 25, "carrera": "TUP", "ciudad": "La Plata"}
# ---------------------------------------------------------------------


def crear_ficha(nombre, edad, **datos_extra):
    ficha = {
        "nombre": nombre,
        "edad": edad
    }

    ficha.update(datos_extra)

    return ficha


ana = crear_ficha(
    "Ana",
    25,
    carrera="Ingeniería",
    ciudad="La Plata"
)

print(ana)


juan = crear_ficha("Juan", 30)

print(juan)
