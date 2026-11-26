# -*- coding: utf-8 -*-
# ---------------------------------------------------------------
# Enunciado 3:
# Escribí una función saludar(nombre, idioma="es") que devuelva
# "Hola, {nombre}!" en español, "Hello, {nombre}!" en inglés,
# o "Ciao, {nombre}!" en italiano.
#
# PREGUNTA: ¿Qué pasa si el idioma no es ninguno de los tres?
#
# PREGUNTA: ¿Qué pasa si no pasamos el segundo parámetro?
# ---------------------------------------------------------------


def saludar(nombre, idioma="es"):
    saludos = {
        "es": "Hola",
        "en": "Hello",
        "it": "Ciao"
    }

    saludo = saludos.get(idioma, "Hola")

    return f"{saludo}, {nombre}!"


print(saludar("Ana"))
print(saludar("John", "en"))
print(saludar("Marco", "it"))
print(saludar("Xx", "cn"))
