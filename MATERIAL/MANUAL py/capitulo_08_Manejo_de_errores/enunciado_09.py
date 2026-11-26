# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 9
# Función acceder_dato(diccionario, clave) que devuelva el valor si
# la clave existe, o el string "[dato faltante]" si no. Usá
# try/except KeyError (después probá con .get() y explicá cuál
# es mejor).
# -------------------------------------------------------------------------


def acceder_dato(diccionario, clave):
    # diccionario[clave] falla con KeyError si la clave no existe.
    # El except captura ese error y retorna el string "[dato faltante]".
    try:
        return diccionario[clave]
    except KeyError:
        return "[dato faltante]"


usuario = {"nombre": "Ana", "edad": 25}
print(acceder_dato(usuario, "nombre"))
print(acceder_dato(usuario, "email"))


# Versión con .get():


def acceder_dato(diccionario, clave):
    return diccionario.get(clave, "[dato faltante]")


print(acceder_dato(usuario, "nombre"))
print(acceder_dato(usuario, "email"))
