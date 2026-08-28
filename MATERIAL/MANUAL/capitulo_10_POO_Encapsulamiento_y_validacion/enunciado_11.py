# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Password con _valor privado. El setter debe verificar:
# al menos 8 caracteres, al menos una mayúscula, una minúscula y un
# dígito. Lanzá excepciones distintas para cada regla (creá tres
# excepciones propias).
# -------------------------------------------------------------------------


class ClaveCortaError(Exception):
    pass


class ClaveSinMayusculaError(Exception):
    pass


class ClaveSinDigitoError(Exception):
    pass


class Password:
    def __init__(self, valor):
        self.valor = valor

    @property
    def valor(self):
        return self._valor

    @valor.setter
    def valor(self, v):
        if len(v) < 8:
            raise ClaveCortaError(
                "Debe tener al menos 8 caracteres"
            )

        if not any(c.isupper() for c in v):
            raise ClaveSinMayusculaError(
                "Debe tener al menos una mayúscula"
            )

        if not any(c.isdigit() for c in v):
            raise ClaveSinDigitoError(
                "Debe tener al menos un dígito"
            )

        self._valor = v


try:
    Password("abc")
except ClaveCortaError as e:
    print(f"Error: {e}")


try:
    Password("abcdefgh")
except ClaveSinMayusculaError as e:
    print(f"Error: {e}")


Password("Password1")  # OK
