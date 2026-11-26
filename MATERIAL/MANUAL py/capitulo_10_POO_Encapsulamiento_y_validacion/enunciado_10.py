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

        # No guardamos directamente:
        # self._email = email
        #
        # Usamos la property:
        # self.email = email
        #
        # De esta manera el setter también valida el email cuando se
        # crea el objeto.
        #
        # Secuencia:
        # Contacto(nombre, email)
        #         ↓
        # __init__()
        #         ↓
        # self.email = email
        #         ↓
        # setter de email
        #         ↓
        # validar cantidad de @
        #         ↓
        # validar que exista un . después de la @
        #         ↓
        # self._email = valor
        self.email = email

    @property
    def email(self):
        # email es la property pública.
        # _email es el atributo interno donde se guarda el valor.
        return self._email

    @email.setter
    def email(self, valor):
        # Primera validación:
        # debe existir exactamente un carácter @.
        #
        # count("@") cuenta cuántas veces aparece @ en el string.
        if valor.count("@") != 1:
            raise EmailInvalidoError(
                "Debe tener exactamente una @"
            )

        # find("@") devuelve la posición donde se encuentra la @.
        #
        # Ejemplo:
        # "ana@correo.com"
        #     ↑
        #     posición de la @
        arroba = valor.find("@")

        # Segunda validación:
        # debe existir al menos un punto después de la @.
        #
        # find(".", arroba) busca un punto comenzando desde la posición
        # de la @.
        #
        # Si no encuentra ningún punto, devuelve -1.
        if valor.find(".", arroba) == -1:
            raise EmailInvalidoError(
                "Debe tener un punto después de la @"
            )

        # El valor se guarda solamente después de superar las dos
        # validaciones.
        #
        # Usamos un solo guion bajo (_email) porque en Python indica,
        # por convención, que el atributo es de uso interno de la clase.
        # Técnicamente puede accederse desde afuera, pero hacerlo
        # significa romper el contrato de la clase.
        #
        # No usamos __email porque el doble guion bajo activa name
        # mangling, usado principalmente para evitar colisiones de
        # nombres en situaciones de herencia.
        self._email = valor


# ---------------------------------------------------------------
# CASO 1: email válido
#
# Contacto("Ana", "ana@correo.com")
#         ↓
# existe exactamente una @
#         ↓
# existe un punto después de la @
#         ↓
# self._email = "ana@correo.com"
# ---------------------------------------------------------------

contacto = Contacto("Ana", "ana@correo.com")

print(contacto.email)  # ana@correo.com


# ---------------------------------------------------------------
# CASO 2: email sin @
#
# "correo.com"
#         ↓
# count("@") devuelve 0
#         ↓
# EmailInvalidoError
# ---------------------------------------------------------------

try:
    contacto_invalido = Contacto("Juan", "correo.com")
except EmailInvalidoError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 3: email con más de una @
#
# "ana@@correo.com"
#         ↓
# count("@") devuelve 2
#         ↓
# EmailInvalidoError
# ---------------------------------------------------------------

try:
    contacto_invalido = Contacto("Ana", "ana@@correo.com")
except EmailInvalidoError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 4: email sin punto después de la @
#
# "pedro@correocom"
#         ↓
# existe exactamente una @
#         ↓
# find(".", arroba) devuelve -1
#         ↓
# EmailInvalidoError
# ---------------------------------------------------------------

try:
    contacto_invalido = Contacto("Pedro", "pedro@correocom")
except EmailInvalidoError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 5: modificación posterior
#
# La property también valida cuando cambiamos el email después de
# haber creado el objeto.
#
# contacto.email = "ana@nuevo.com"
#         ↓
# setter
#         ↓
# validaciones
#         ↓
# self._email = "ana@nuevo.com"
# ---------------------------------------------------------------

try:
    contacto.email = "ana@nuevo.com"
    print(contacto.email)  # ana@nuevo.com
except EmailInvalidoError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 6: intento de modificación con un email inválido
#
# El objeto ya existe, pero el setter vuelve a aplicar las mismas
# validaciones.
# ---------------------------------------------------------------

try:
    contacto.email = "correo-invalido"
except EmailInvalidoError as error:
    print(f"Error: {error}")


# Como el nuevo valor fue rechazado, el email anterior se conserva.
print(contacto.email)  # ana@nuevo.com
