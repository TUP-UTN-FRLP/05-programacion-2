# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 8
# Función abrir_configuracion(nombre_archivo) que intente abrir un
# archivo, devolver el contenido, o un string vacío si no existe.
# Manejar FileNotFoundError. (Podés simularlo llamando la función
# con un nombre inventado.)
# -------------------------------------------------------------------------


def abrir_configuracion(nombre_archivo):
    # open() falla con FileNotFoundError si el archivo no existe.
    # El except captura ese error y retorna {} como valor seguro.
    try:
        with open(nombre_archivo) as f:
            return f.read()
    except FileNotFoundError:
        return {}


config = abrir_configuracion("no_existe.txt")
print(config)
