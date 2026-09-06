# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Usá re para extraer todos los emails de un texto largo. Compilá el
# patrón una sola vez con re.compile: cuando el mismo patrón se usa
# muchas veces, compilarlo evita rehacer el trabajo en cada llamada y
# además le pone nombre a la intención. Fijate que el objeto que devuelve
# re.compile es un re.Pattern con sus propios métodos.
# -------------------------------------------------------------------------

import re

PATRON_EMAIL = re.compile(r"[\w.-]+@[\w.-]+\.\w+")


def extraer_emails(texto):
    """Devuelve todos los emails que aparecen en el texto."""
    return PATRON_EMAIL.findall(texto)


if __name__ == "__main__":
    texto = (
        "Contactame en ana.perez@correo.com o en "
        "pedro_lopez@ejemplo.com.ar. También podés "
        "escribirle a Juan (juan99@fake.co) o al "
        "soporte@empresa.io."
    )

    for email in extraer_emails(texto):
        print(f"  {email}")

    print(type(PATRON_EMAIL))
    print(PATRON_EMAIL.pattern)
