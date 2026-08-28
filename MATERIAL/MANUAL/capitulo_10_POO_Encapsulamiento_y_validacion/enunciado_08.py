# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Estudiante con nombre (privado, solo lectura) y una
# lista privada _notas. Métodos: agregar_nota(nota) que valide que la
# nota esté entre 0 y 10, promedio como property de solo lectura.
# -------------------------------------------------------------------------


class Estudiante:
    def __init__(self, nombre):
        # El nombre se guarda como atributo interno y será de solo
        # lectura porque solamente lo expondremos mediante @property.
        self._nombre = nombre

        # _notas es una lista interna que comienza vacía.
        #
        # Usamos un solo guion bajo porque en Python indica, por
        # convención, que el atributo es de uso interno de la clase.
        # Técnicamente podría accederse a estudiante._notas desde afuera,
        # pero hacerlo significaría romper el contrato de la clase.
        #
        # No usamos __notas porque el doble guion bajo activa name
        # mangling, usado principalmente para evitar colisiones de
        # nombres en situaciones de herencia.
        self._notas = []

    @property
    def nombre(self):
        # nombre es una property de solo lectura.
        # Como no existe @nombre.setter, no se puede modificar mediante:
        # estudiante.nombre = "Otro nombre"
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

        # La nota se incorpora solamente después de superar todas las
        # validaciones.
        self._notas.append(nota)

    @property
    def promedio(self):
        # promedio es una property de solo lectura.
        #
        # No existe un atributo _promedio porque no necesitamos guardar
        # ese dato. Se calcula cada vez que se consulta.
        #
        # Si todavía no hay notas, devolvemos 0 para evitar una división
        # por cero.
        if not self._notas:
            return 0

        # El promedio puede tener decimales aunque las notas individuales
        # sean enteras.
        return sum(self._notas) / len(self._notas)


# ---------------------------------------------------------------
# CASO 1: creación del estudiante
#
# Al crearlo:
# _nombre = "Ana"
# _notas = []
# ---------------------------------------------------------------

ana = Estudiante("Ana")

print(ana.nombre)  # Ana
print(ana.promedio)  # 0


# ---------------------------------------------------------------
# CASO 2: agregar notas válidas
#
# agregar_nota(8)
#         ↓
# 8 es entero
#         ↓
# está entre 0 y 10
#         ↓
# _notas.append(8)
# ---------------------------------------------------------------

ana.agregar_nota(8)
ana.agregar_nota(9)

# Las notas son enteras, pero el promedio puede ser decimal:
#
# (8 + 9) / 2
#       ↓
# 17 / 2
#       ↓
# 8.5
print(ana.promedio)  # 8.5


# ---------------------------------------------------------------
# CASO 3: intento de agregar una nota con decimales
#
# agregar_nota(8.5)
#         ↓
# 8.5 no es int
#         ↓
# TypeError
# ---------------------------------------------------------------

try:
    ana.agregar_nota(8.5)
except TypeError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 4: intento de agregar una nota fuera de rango
#
# agregar_nota(12)
#         ↓
# 12 es entero
#         ↓
# no está entre 0 y 10
#         ↓
# ValueError
# ---------------------------------------------------------------

try:
    ana.agregar_nota(12)
except ValueError as error:
    print(f"Error: {error}")


# Las notas inválidas no fueron incorporadas, por lo que el promedio
# continúa siendo el mismo.
print(ana.promedio)  # 8.5
