# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Escribí contrasenia_segura(longitud) que genere una contraseña con
# letras mayúsculas, minúsculas y dígitos. Importante: NO uses random.
# El módulo random es predecible y no sirve para secretos; para eso está
# secrets, que usa la fuente de aleatoriedad del sistema operativo.
# Compará las dos versiones y explicá la diferencia en un comentario.
# -------------------------------------------------------------------------

import secrets
import string


def contrasenia_segura(longitud):
    """Genera una contraseña criptográficamente segura."""
    if longitud < 8:
        raise ValueError("La contraseña debe tener 8 o más")

    alfabeto = string.ascii_letters + string.digits

    return "".join(
        secrets.choice(alfabeto) for _ in range(longitud)
    )


def token_de_sesion():
    """Devuelve un token hexadecimal listo para usar en una URL."""
    return secrets.token_hex(16)


if __name__ == "__main__":
    # random.choices() reproduce la misma secuencia si alguien
    # conoce la semilla, así que una contraseña generada con random
    # es adivinable. secrets no expone semilla ni estado interno.
    print(contrasenia_segura(12))
    print(token_de_sesion())

    try:
        contrasenia_segura(4)
    except ValueError as error:
        print(f"Error: {error}")
