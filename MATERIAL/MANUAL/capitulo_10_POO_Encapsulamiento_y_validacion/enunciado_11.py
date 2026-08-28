# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Password con _valor privado. El setter debe verificar:
# al menos 8 caracteres, al menos una mayúscula, una minúscula y un
# dígito. Lanzá excepciones distintas para cada regla.
# -------------------------------------------------------------------------


class ClaveCortaError(Exception):
    pass


class ClaveSinMayusculaError(Exception):
    pass


class ClaveSinMinusculaError(Exception):
    pass


class ClaveSinDigitoError(Exception):
    pass


class Password:
    def __init__(self, valor):
        # No guardamos directamente:
        # self._valor = valor
        #
        # Usamos la property:
        # self.valor = valor
        #
        # Esto hace que el setter valide la contraseña también cuando
        # se crea el objeto.
        #
        # Secuencia:
        # Password(valor)
        #       ↓
        # __init__()
        #       ↓
        # self.valor = valor
        #       ↓
        # setter de valor
        #       ↓
        # validar longitud
        #       ↓
        # validar mayúscula
        #       ↓
        # validar minúscula
        #       ↓
        # validar dígito
        #       ↓
        # self._valor = valor
        self.valor = valor

    @property
    def valor(self):
        # valor es la property pública.
        # _valor es el atributo interno donde se guarda la contraseña.
        return self._valor

    @valor.setter
    def valor(self, valor):
        # Primera validación:
        # la contraseña debe tener al menos 8 caracteres.
        if len(valor) < 8:
            raise ClaveCortaError(
                "Debe tener al menos 8 caracteres"
            )

        # Segunda validación:
        # debe contener al menos una letra mayúscula.
        #
        # isupper() se aplica a cada carácter.
        # any() devuelve True apenas encuentra una mayúscula.
        if not any(caracter.isupper() for caracter in valor):
            raise ClaveSinMayusculaError(
                "Debe tener al menos una mayúscula"
            )

        # Tercera validación:
        # debe contener al menos una letra minúscula.
        if not any(caracter.islower() for caracter in valor):
            raise ClaveSinMinusculaError(
                "Debe tener al menos una minúscula"
            )

        # Cuarta validación:
        # debe contener al menos un dígito.
        if not any(caracter.isdigit() for caracter in valor):
            raise ClaveSinDigitoError(
                "Debe tener al menos un dígito"
            )

        # El valor se guarda solamente después de superar todas las
        # validaciones.
        #
        # Usamos un solo guion bajo (_valor) porque en Python indica, por
        # convención, que el atributo es de uso interno de la clase.
        # Técnicamente puede accederse desde afuera, pero hacerlo
        # significa romper el contrato de la clase.
        #
        # No usamos __valor porque el doble guion bajo activa name
        # mangling, usado principalmente para evitar colisiones de
        # nombres en situaciones de herencia.
        self._valor = valor


# ---------------------------------------------------------------
# CASO 1: contraseña demasiado corta
#
# "Abc1"
#       ↓
# tiene menos de 8 caracteres
#       ↓
# ClaveCortaError
# ---------------------------------------------------------------

try:
    password = Password("Abc1")
except ClaveCortaError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 2: contraseña sin mayúsculas
#
# "abcdefg1"
#       ↓
# supera la longitud mínima
#       ↓
# ninguna letra cumple isupper()
#       ↓
# ClaveSinMayusculaError
# ---------------------------------------------------------------

try:
    password = Password("abcdefg1")
except ClaveSinMayusculaError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 3: contraseña sin minúsculas
#
# "ABCDEFG1"
#       ↓
# tiene mayúsculas
#       ↓
# ninguna letra cumple islower()
#       ↓
# ClaveSinMinusculaError
# ---------------------------------------------------------------

try:
    password = Password("ABCDEFG1")
except ClaveSinMinusculaError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 4: contraseña sin dígitos
#
# "Password"
#       ↓
# tiene mayúsculas y minúsculas
#       ↓
# ningún carácter cumple isdigit()
#       ↓
# ClaveSinDigitoError
# ---------------------------------------------------------------

try:
    password = Password("Password")
except ClaveSinDigitoError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 5: contraseña válida
#
# "Password1"
#       ↓
# tiene al menos 8 caracteres
#       ↓
# tiene mayúscula
#       ↓
# tiene minúscula
#       ↓
# tiene dígito
#       ↓
# se guarda en self._valor
# ---------------------------------------------------------------

try:
    password = Password("Password1")
    print("Contraseña válida")
except (
    ClaveCortaError,
    ClaveSinMayusculaError,
    ClaveSinMinusculaError,
    ClaveSinDigitoError,
) as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 6: modificación posterior
#
# Como valor es una property con setter, las mismas validaciones se
# aplican cuando intentamos cambiar la contraseña.
# ---------------------------------------------------------------

try:
    password.valor = "NuevaClave2"
    print("Contraseña modificada correctamente")
except (
    ClaveCortaError,
    ClaveSinMayusculaError,
    ClaveSinMinusculaError,
    ClaveSinDigitoError,
) as error:
    print(f"Error: {error}")
