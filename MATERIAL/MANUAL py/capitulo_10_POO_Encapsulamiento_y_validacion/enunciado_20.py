# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Persona con nombre, apellido y dni privados. Validá en
# el __init__: nombre y apellido no vacíos, DNI de 7 u 8 dígitos
# numéricos. Property nombre_completo de solo lectura que devuelva
# "Apellido, Nombre".
# -------------------------------------------------------------------------


class Persona:
    def __init__(self, nombre, apellido, dni):
        # Todas las validaciones se realizan antes de guardar los datos.
        #
        # Secuencia:
        # Persona(nombre, apellido, dni)
        #         ↓
        # validar nombre
        #         ↓
        # validar apellido
        #         ↓
        # validar DNI
        #         ↓
        # limpiar y normalizar nombre y apellido
        #         ↓
        # guardar los atributos internos

        # nombre debe ser un string y no puede quedar vacío después de
        # eliminar los espacios de los extremos.
        if not isinstance(nombre, str):
            raise TypeError("El nombre debe ser un string")

        if not nombre.strip():
            raise ValueError("El nombre no puede estar vacío")

        # Aplicamos las mismas validaciones al apellido.
        if not isinstance(apellido, str):
            raise TypeError("El apellido debe ser un string")

        if not apellido.strip():
            raise ValueError("El apellido no puede estar vacío")

        # El DNI se maneja como string porque es un identificador, no un
        # número con el que vayamos a realizar operaciones matemáticas.
        #
        # Debe cumplir tres condiciones:
        # - ser un string;
        # - contener solamente dígitos;
        # - tener 7 u 8 caracteres.
        if not isinstance(dni, str):
            raise TypeError("El DNI debe ser un string")

        if not dni.isdigit() or len(dni) not in (7, 8):
            raise ValueError(
                "DNI debe ser 7 u 8 dígitos numéricos"
            )

        # Los datos se guardan solamente después de superar todas las
        # validaciones.
        #
        # strip() elimina espacios de los extremos.
        # title() coloca en mayúscula la inicial de cada palabra.
        self._nombre = nombre.strip().title()
        self._apellido = apellido.strip().title()
        self._dni = dni

        # Usamos un solo guion bajo porque en Python indica, por
        # convención, que estos atributos son de uso interno de la clase.
        # Técnicamente pueden accederse desde afuera, pero hacerlo
        # significa romper el contrato de la clase.
        #
        # No usamos __nombre, __apellido o __dni porque el doble guion
        # bajo activa name mangling, usado principalmente para evitar
        # colisiones de nombres en situaciones de herencia.

    @property
    def nombre(self):
        # nombre es una property de solo lectura.
        # Como no existe @nombre.setter, no puede asignarse directamente.
        return self._nombre

    @property
    def apellido(self):
        # apellido también es una property de solo lectura.
        return self._apellido

    @property
    def dni(self):
        # dni puede consultarse, pero no modificarse mediante la
        # interfaz pública.
        return self._dni

    @property
    def nombre_completo(self):
        # nombre_completo es una property calculada.
        #
        # No existe un atributo _nombre_completo porque el valor puede
        # construirse utilizando _apellido y _nombre cada vez que se
        # consulta.
        return f"{self._apellido}, {self._nombre}"

    def __str__(self):
        # Reutilizamos la property nombre_completo en lugar de repetir
        # la misma lógica.
        return f"{self.nombre_completo} (DNI {self._dni})"


# ---------------------------------------------------------------
# CASO 1: creación de una persona válida
#
# Persona("ana", "pérez", "12345678")
#         ↓
# nombre válido
#         ↓
# apellido válido
#         ↓
# DNI válido
#         ↓
# nombre → "Ana"
# apellido → "Pérez"
# ---------------------------------------------------------------

persona = Persona("ana", "pérez", "12345678")

print(persona.nombre)  # Ana
print(persona.apellido)  # Pérez
print(persona.dni)  # 12345678
print(persona.nombre_completo)  # Pérez, Ana
print(persona)  # Pérez, Ana (DNI 12345678)


# ---------------------------------------------------------------
# CASO 2: normalización de nombre y apellido
#
# strip() elimina espacios de los extremos.
# title() coloca las iniciales en mayúscula.
# ---------------------------------------------------------------

persona_2 = Persona(
    "   juan carlos   ",
    "   gonzález   ",
    "1234567",
)

print(persona_2.nombre_completo)  # González, Juan Carlos


# ---------------------------------------------------------------
# CASO 3: DNI con caracteres que no son dígitos
#
# dni = "abc"
#       ↓
# isdigit() devuelve False
#       ↓
# ValueError
# ---------------------------------------------------------------

try:
    persona_invalida = Persona("Ana", "Pérez", "abc")
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 4: DNI numérico pero demasiado corto
#
# "123"
#       ↓
# contiene solamente dígitos
#       ↓
# pero no tiene 7 u 8 caracteres
#       ↓
# ValueError
# ---------------------------------------------------------------

try:
    persona_invalida = Persona("Ana", "Pérez", "123")
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 5: nombre vacío
# ---------------------------------------------------------------

try:
    persona_invalida = Persona("   ", "Pérez", "12345678")
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 6: apellido vacío
# ---------------------------------------------------------------

try:
    persona_invalida = Persona("Ana", "   ", "12345678")
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 7: DNI recibido como entero
#
# Aunque visualmente parezca un número correcto, el diseño de la clase
# establece que el DNI se recibe como string.
# ---------------------------------------------------------------

try:
    persona_invalida = Persona("Ana", "Pérez", 12345678)
except TypeError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 8: intento de modificar una property de solo lectura
#
# persona.nombre = "María"
#         ↓
# Python busca @nombre.setter
#         ↓
# no existe
#         ↓
# AttributeError
# ---------------------------------------------------------------

try:
    persona.nombre = "María"
except AttributeError as error:
    print(f"Error: {error}")


# El nombre original se conserva.
print(persona.nombre_completo)  # Pérez, Ana
