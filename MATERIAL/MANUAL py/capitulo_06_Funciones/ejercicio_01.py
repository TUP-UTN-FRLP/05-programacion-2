# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------
# Escribí una función mostrar_titulo(texto) que imprima el texto en
# mayúsculas
# rodeado de líneas de guiones. Después llamala tres veces con títulos
# distintos.
# -----------------------------------------------------------------------


def mostrar_titulo(texto):
    print("-" * 30)
    print(texto.upper().center(30))
    print("-" * 30)


mostrar_titulo("Bienvenido")
mostrar_titulo("Menú principal")
mostrar_titulo("Fin del programa")
