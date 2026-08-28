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

        # No guardamos directamente:
        #
        # self._contraseña = contraseña
        #
        # Usamos la property:
        #
        # self.contraseña = contraseña
        #
        # Esto provoca que el setter se ejecute también durante la
        # creación del objeto.
        #
        # Secuencia:
        #
        # Usuario(nombre, contraseña)
        #         ↓
        # __init__()
        #         ↓
        # self.contraseña = contraseña
        #         ↓
        # setter de contraseña
        #         ↓
        # validar longitud
        #         ↓
        # validar que exista un dígito
        #         ↓
        # self._contraseña = valor
        self.contraseña = contraseña

    @property
    def contraseña(self):
        # contraseña es la property pública.
        # _contraseña es el atributo interno donde se guarda el valor.
        return self._contraseña

    @contraseña.setter
    def contraseña(self, valor):
        # Este setter se ejecuta automáticamente tanto al crear el
        # objeto como al hacer posteriormente:
        #
        # usuario.contraseña = "NuevaClave123"

        # Primera validación:
        # la contraseña debe tener al menos 8 caracteres.
        if len(valor) < 8:
            raise ContraseñaDebilError(
                "Debe tener al menos 8 caracteres"
            )

        # Segunda validación:
        # debe existir al menos un carácter que sea un dígito.
        #
        # La expresión:
        #
        # c.isdigit() for c in valor
        #
        # revisa los caracteres de la contraseña uno por uno.
        #
        # any() devuelve True apenas encuentra un dígito.
        if not any(c.isdigit() for c in valor):
            raise ContraseñaDebilError(
                "Debe contener al menos un dígito"
            )

        # Si llegamos hasta acá, las dos validaciones fueron superadas.
        #
        # Recién entonces guardamos el valor en el atributo interno.
        #
        # Usamos un solo guion bajo (_contraseña) porque en Python esta
        # es la convención para indicar que un atributo es de uso interno
        # de la clase.
        #
        # Técnicamente podría accederse desde afuera con
        # usuario._contraseña, pero hacerlo significa romper el contrato
        # de la clase.
        #
        # No usamos __contraseña porque el doble guion bajo activa name
        # mangling, mecanismo reservado principalmente para evitar
        # colisiones de nombres en situaciones de herencia.
        self._contraseña = valor


# ---------------------------------------------------------------
# CASO 1: contraseña demasiado corta
#
# Usuario("Ana", "corta")
#         ↓
# __init__()
#         ↓
# setter de contraseña
#         ↓
# len("corta") < 8
#         ↓
# ContraseñaDebilError
# ---------------------------------------------------------------

try:
    usuario = Usuario("Ana", "corta")
except ContraseñaDebilError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 2: tiene 8 o más caracteres, pero no contiene ningún dígito
#
# "contraseña"
#         ↓
# supera la validación de longitud
#         ↓
# ningún carácter cumple isdigit()
#         ↓
# ContraseñaDebilError
# ---------------------------------------------------------------

try:
    usuario = Usuario("Ana", "contraseña")
except ContraseñaDebilError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 3: contraseña válida
#
# "clave123"
#         ↓
# tiene al menos 8 caracteres
#         ↓
# contiene dígitos
#         ↓
# se guarda en self._contraseña
# ---------------------------------------------------------------

try:
    usuario = Usuario("Ana", "clave123")
    print("Usuario creado correctamente")
except ContraseñaDebilError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 4: modificación posterior
#
# La property también protege los cambios realizados después de crear
# el objeto.
#
# usuario.contraseña = "otra456"
#         ↓
# setter
#         ↓
# validaciones
#         ↓
# self._contraseña = "otra456"
# ---------------------------------------------------------------

try:
    usuario.contraseña = "otra456"
    print("Contraseña modificada correctamente")
except ContraseñaDebilError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 5: intento de modificación con una contraseña inválida
#
# El objeto ya existe, pero el setter vuelve a aplicar exactamente las
# mismas reglas.
# ---------------------------------------------------------------

try:
    usuario.contraseña = "sinNumero"
except ContraseñaDebilError as error:
    print(f"Error: {error}")
