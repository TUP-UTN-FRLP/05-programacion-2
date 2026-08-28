# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Libro con titulo, autor y paginas, más un _leido
# privado (booleano, arranca en False) expuesto como property de solo
# lectura. Método marcar_como_leido() que lo pone en True, y
# desmarcar() que lo pone en False.
# -------------------------------------------------------------------------


class Libro:
    def __init__(self, titulo, autor, paginas):
        # Validamos primero los datos recibidos antes de guardarlos.
        #
        # Secuencia:
        # Libro(titulo, autor, paginas)
        #         ↓
        # validar titulo
        #         ↓
        # validar autor
        #         ↓
        # validar paginas
        #         ↓
        # guardar los atributos internos
        #         ↓
        # iniciar _leido en False

        # titulo debe ser un string y no puede quedar vacío después de
        # eliminar los espacios de los extremos.
        if not isinstance(titulo, str) or not titulo.strip():
            raise ValueError("El título no puede estar vacío")

        # Aplicamos la misma regla al autor.
        if not isinstance(autor, str) or not autor.strip():
            raise ValueError("El autor no puede estar vacío")

        # La cantidad de páginas representa unidades completas.
        # Por eso debe ser un número entero.
        if type(paginas) is not int:
            raise TypeError("La cantidad de páginas debe ser un entero")

        if paginas <= 0:
            raise ValueError("Debe tener al menos 1 página")

        # Los datos se guardan solamente después de superar todas las
        # validaciones.
        self._titulo = titulo.strip()
        self._autor = autor.strip()
        self._paginas = paginas

        # Todo libro comienza marcado como no leído.
        #
        # _leido es un atributo interno de tipo booleano:
        # False → sin leer
        # True  → leído
        self._leido = False

        # Usamos un solo guion bajo en los atributos porque en Python
        # indica, por convención, que son de uso interno de la clase.
        # Técnicamente pueden accederse desde afuera, pero hacerlo
        # significa romper el contrato de la clase.
        #
        # No usamos __leido porque el doble guion bajo activa name
        # mangling, usado principalmente para evitar colisiones de
        # nombres en situaciones de herencia.

    @property
    def leido(self):
        # leido es una property de solo lectura.
        #
        # Desde afuera podemos consultar:
        # libro.leido
        #
        # pero no podemos hacer:
        # libro.leido = True
        #
        # porque no existe @leido.setter.
        return self._leido

    def marcar_como_leido(self):
        # Este método pertenece a la propia clase, por lo que puede
        # modificar directamente el atributo interno.
        #
        # marcar_como_leido()
        #         ↓
        # self._leido = True
        self._leido = True

    def desmarcar(self):
        # Volvemos el estado interno a False.
        self._leido = False

    def __str__(self):
        # Elegimos el texto a mostrar según el valor booleano de _leido.
        estado = "leído" if self._leido else "sin leer"

        return (
            f"'{self._titulo}' de {self._autor} "
            f"({self._paginas} páginas, {estado})"
        )


# ---------------------------------------------------------------
# CASO 1: creación de un libro válido
#
# Libro("El Aleph", "Borges", 224)
#         ↓
# datos válidos
#         ↓
# _leido = False
# ---------------------------------------------------------------

libro = Libro("El Aleph", "Borges", 224)

print(libro)
# 'El Aleph' de Borges (224 páginas, sin leer)

print(libro.leido)  # False


# ---------------------------------------------------------------
# CASO 2: marcar el libro como leído
#
# marcar_como_leido()
#         ↓
# self._leido = True
# ---------------------------------------------------------------

libro.marcar_como_leido()

print(libro)
# 'El Aleph' de Borges (224 páginas, leído)

print(libro.leido)  # True


# ---------------------------------------------------------------
# CASO 3: desmarcar el libro
#
# desmarcar()
#         ↓
# self._leido = False
# ---------------------------------------------------------------

libro.desmarcar()

print(libro)
# 'El Aleph' de Borges (224 páginas, sin leer)

print(libro.leido)  # False


# ---------------------------------------------------------------
# CASO 4: intento de modificar leido directamente
#
# libro.leido = True
#         ↓
# Python encuentra la property leido
#         ↓
# busca @leido.setter
#         ↓
# no existe
#         ↓
# AttributeError
# ---------------------------------------------------------------

try:
    libro.leido = True
except AttributeError as error:
    print(f"Error: {error}")


# El intento anterior no modificó el estado.
print(libro.leido)  # False


# ---------------------------------------------------------------
# CASO 5: título vacío
# ---------------------------------------------------------------

try:
    libro_invalido = Libro("   ", "Borges", 224)
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 6: autor vacío
# ---------------------------------------------------------------

try:
    libro_invalido = Libro("El Aleph", "   ", 224)
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 7: cantidad de páginas inválida
#
# El tipo es correcto, pero el valor no sirve.
# ---------------------------------------------------------------

try:
    libro_invalido = Libro("El Aleph", "Borges", 0)
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 8: páginas con un tipo incorrecto
# ---------------------------------------------------------------

try:
    libro_invalido = Libro("El Aleph", "Borges", 224.5)
except TypeError as error:
    print(f"Error: {error}")
