# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 15
# Función parsear_fecha(texto) que reciba una fecha tipo "25/07/2026"
# y devuelva una tupla (día, mes, año) con enteros. Si el formato es
# inválido, lanzá ValueError con mensaje claro.
# -------------------------------------------------------------------------


def parsear_fecha(texto):
    # int() falla con ValueError si alguna parte no es numérica.
    # raise lanza ValueError manualmente si el formato no tiene 3 partes.
    # El except los envuelve en un nuevo ValueError con más contexto.
    try:
        partes = texto.split("/")

        if len(partes) != 3:
            raise ValueError("Formato inválido, se esperaba dd/mm/aaaa")

        dia = int(partes[0])
        mes = int(partes[1])
        año = int(partes[2])

        return dia, mes, año

    except ValueError as e:
        raise ValueError(f"No se pudo parsear '{texto}': {e}")


# parsear_fecha() lanza ValueError si el texto tiene formato inválido.
# El except captura ese error y muestra el mensaje sin cortar el programa.
try:
    print(parsear_fecha("25/07/2026"))
    print(parsear_fecha("25-07-2026"))
except ValueError as e:
    print(e)
