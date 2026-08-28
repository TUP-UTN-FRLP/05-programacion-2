# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Creá una excepción EmailInvalidoError. Hacé una clase Contacto con
# nombre y _email privado. Validá el email en el setter: debe tener
# exactamente una @ y al menos un . después de la @.
# -------------------------------------------------------------------------


class EmailInvalidoError(Exception):
    """Se lanza cuando un email no tiene formato válido."""

    pass


class Contacto:
    def __init__(self, nombre, email):
        self._nombre = nombre
        self.email = email

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if valor.count("@") != 1:
            raise EmailInvalidoError(
                "Debe tener exactamente una @"
            )

        arroba = valor.find("@")

        if valor.find(".", arroba) == -1:
            raise EmailInvalidoError(
                "Debe tener un punto después de la @"
            )

        self._email = valor


c = Contacto("Ana", "ana@correo.com")  # OK

Contacto("Juan", "correo.com")  # EmailInvalidoError

Contacto("Pedro", "pedro@correocom")  # EmailInvalidoError
