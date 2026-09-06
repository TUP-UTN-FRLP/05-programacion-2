# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Escribí un módulo de validaciones con es_dni_valido(dni) y
# normalizar_nombre(nombre), y poné toda la prueba dentro de
# if __name__ == "__main__":. Imprimí el valor de __name__ para ver la
# diferencia: si ejecutás el archivo vale "__main__" y la prueba corre;
# si otro archivo hace "import ejercicio_04", vale "ejercicio_04" y la
# prueba no corre.
# -------------------------------------------------------------------------

def es_dni_valido(dni):
    """Indica si el DNI es una cadena de 7 u 8 dígitos."""
    return (
        isinstance(dni, str)
        and dni.isdigit()
        and len(dni) in (7, 8)
    )


def normalizar_nombre(nombre):
    """Devuelve el nombre sin espacios sobrantes y capitalizado."""
    return nombre.strip().title()


if __name__ == "__main__":
    print(f'__name__ vale "{__name__}"')

    for dni in ["12345678", "1234", "12a45678", 12345678]:
        print(f"  {dni!r}: {es_dni_valido(dni)}")

    print(normalizar_nombre("  ana maría pérez  "))
