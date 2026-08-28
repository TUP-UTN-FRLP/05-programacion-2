# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Creá una excepción ContraseñaDebilError. Después hacé una clase Usuario
# con nombre y _contraseña privada. El setter de contraseña debe
# rechazar (con la excepción propia) contraseñas de menos de 8
# caracteres o sin al menos un dígito.
# -------------------------------------------------------------------------


class ContraseñaDebilError(Exception):
    """Se lanza cuando una contraseña no cumple los requisitos mínimos."""

    pass


class Usuario:
    def __init__(self, nombre, contraseña):
        self._nombre = nombre
        self.contraseña = contraseña

    @property
    def contraseña(self):
        return self._contraseña

    @contraseña.setter
    def contraseña(self, valor):
        if len(valor) < 8:
            raise ContraseñaDebilError(
                "Debe tener al menos 8 caracteres"
            )

        if not any(c.isdigit() for c in valor):
            raise ContraseñaDebilError(
                "Debe contener al menos un dígito"
            )

        self._contraseña = valor


try:
    u = Usuario("ana", "corta")
except ContraseñaDebilError as e:
    print(e)  # Debe tener al menos 8 caracteres
