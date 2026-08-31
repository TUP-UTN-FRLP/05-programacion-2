# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Sumale a Estudiante una property mejor_nota (solo lectura) y un método
# borrar_ultima_nota() que devuelva la nota borrada, o lance IndexError
# si no hay notas.
# -------------------------------------------------------------------------


class Estudiante:
    def __init__(self, nombre):
        # El nombre se guarda como atributo interno y será de solo
        # lectura porque no tendrá setter.
        self._nombre = nombre

        # _notas es una lista interna que comienza vacía.
        # Usamos un solo guion bajo porque en Python indica, por
        # convención, que el atributo es de uso interno de la clase.
        # No usamos __notas porque el doble guion bajo activa name
        # mangling, usado principalmente para evitar colisiones de
        # nombres en situaciones de herencia.
        self._notas = []

    @property
    def nombre(self):
        # Como no existe @nombre.setter, nombre es de solo lectura.
        return self._nombre

    def agregar_nota(self, nota):
        # Las notas deben ser números enteros, sin decimales.
        #
        # Secuencia:
        # agregar_nota(nota)
        #         ↓
        # validar que sea un entero
        #         ↓
        # validar que esté entre 0 y 10
        #         ↓
        # agregarla a _notas
        if type(nota) is not int:
            raise TypeError("La nota debe ser un número entero")

        if not 0 <= nota <= 10:
            raise ValueError("La nota debe estar entre 0 y 10")

        self._notas.append(nota)

    @property
    def promedio(self):
        # Si no hay notas, devolvemos 0 para evitar dividir por cero.
        if not self._notas:
            return 0

        # Las notas son enteras, pero el promedio puede ser decimal.
        return sum(self._notas) / len(self._notas)

    @property
    def mejor_nota(self):
        # mejor_nota es una property de solo lectura.
        #
        # Si no hay notas, devolvemos None porque todavía no existe una
        # nota que pueda considerarse la mejor.
        if not self._notas:
            return None

        # max() devuelve el valor más alto de la lista.
        return max(self._notas)

    def borrar_ultima_nota(self):
        # Antes de borrar verificamos que la lista tenga elementos.
        #
        # Si la lista está vacía no existe una última nota y lanzamos
        # IndexError.
        if not self._notas:
            raise IndexError("No hay notas para borrar")

        # pop() sin indicar posición elimina el último elemento de la
        # lista y además devuelve el valor eliminado.
        return self._notas.pop()


# ---------------------------------------------------------------
# CASO 1: creación del estudiante
# ---------------------------------------------------------------

ana = Estudiante("Ana")

print(ana.nombre)  # Ana
print(ana.promedio)  # 0
print(ana.mejor_nota)  # None


# ---------------------------------------------------------------
# CASO 2: agregar notas válidas
#
# _notas comienza así:
# []
#
# Después:
# agregar_nota(8) → [8]
# agregar_nota(9) → [8, 9]
# agregar_nota(7) → [8, 9, 7]
# ---------------------------------------------------------------

ana.agregar_nota(8)
ana.agregar_nota(9)
ana.agregar_nota(7)

print(ana.mejor_nota)  # 9


# ---------------------------------------------------------------
# CASO 3: borrar la última nota
#
# _notas = [8, 9, 7]
#         ↓
# pop()
#         ↓
# devuelve 7
#         ↓
# _notas queda [8, 9]
# ---------------------------------------------------------------

nota_borrada = ana.borrar_ultima_nota()

print(f"Nota borrada: {nota_borrada}")  # Nota borrada: 7
print(ana.mejor_nota)  # 9
print(ana.promedio)  # 8.5


# ---------------------------------------------------------------
# CASO 4: borrar nuevamente
#
# _notas = [8, 9]
#         ↓
# pop()
#         ↓
# devuelve 9
#         ↓
# _notas queda [8]
#
# Ahora la mejor nota también cambia.
# ---------------------------------------------------------------

nota_borrada = ana.borrar_ultima_nota()

print(f"Nota borrada: {nota_borrada}")  # Nota borrada: 9
print(ana.mejor_nota)  # 8
print(ana.promedio)  # 8.0


# ---------------------------------------------------------------
# CASO 5: borrar la última nota disponible
# ---------------------------------------------------------------

nota_borrada = ana.borrar_ultima_nota()

print(f"Nota borrada: {nota_borrada}")  # Nota borrada: 8
print(ana.mejor_nota)  # None
print(ana.promedio)  # 0


# ---------------------------------------------------------------
# CASO 6: intentar borrar cuando ya no hay notas
#
# _notas = []
#         ↓
# borrar_ultima_nota()
#         ↓
# la lista está vacía
#         ↓
# IndexError
# ---------------------------------------------------------------

try:
    ana.borrar_ultima_nota()
except IndexError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 7: intento de agregar una nota con decimales
# ---------------------------------------------------------------

try:
    ana.agregar_nota(8.5)
except TypeError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 8: intento de agregar una nota fuera de rango
# ---------------------------------------------------------------

try:
    ana.agregar_nota(11)
except ValueError as error:
    print(f"Error: {error}")
