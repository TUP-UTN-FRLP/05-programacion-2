# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Empleado con _sueldo_basico privado y expuesto como
# property. El setter debe rechazar sueldos negativos. Sumale un método
# aumentar_sueldo(porcentaje) que valide que el porcentaje sea positivo.
# -------------------------------------------------------------------------


class Empleado:
    def __init__(self, nombre, sueldo_basico):
        self._nombre = nombre

        # No guardamos directamente:
        # self._sueldo_basico = sueldo_basico
        #
        # Usamos la property:
        # self.sueldo_basico = sueldo_basico
        #
        # Esto provoca que el setter se ejecute también al crear el
        # objeto.
        #
        # Secuencia:
        # Empleado(nombre, sueldo_basico)
        #         ↓
        # __init__()
        #         ↓
        # self.sueldo_basico = sueldo_basico
        #         ↓
        # setter de sueldo_basico
        #         ↓
        # validar que el sueldo no sea negativo
        #         ↓
        # self._sueldo_basico = valor
        self.sueldo_basico = sueldo_basico

    @property
    def sueldo_basico(self):
        # sueldo_basico es la property pública.
        # _sueldo_basico es el atributo interno donde se guarda el valor.
        return self._sueldo_basico

    @sueldo_basico.setter
    def sueldo_basico(self, valor):
        # Este setter se ejecuta automáticamente cuando hacemos:
        # empleado.sueldo_basico = valor
        #
        # También se ejecuta desde __init__ porque allí usamos:
        # self.sueldo_basico = sueldo_basico
        if valor < 0:
            raise ValueError("El sueldo no puede ser negativo")

        # El valor se guarda solamente después de superar la validación.
        #
        # Usamos un solo guion bajo (_sueldo_basico) porque en Python
        # indica, por convención, que el atributo es de uso interno de
        # la clase.
        #
        # Técnicamente se podría acceder a empleado._sueldo_basico desde
        # afuera, pero hacerlo significa romper el contrato de la clase.
        #
        # No usamos __sueldo_basico porque el doble guion bajo activa
        # name mangling, mecanismo usado principalmente para evitar
        # colisiones de nombres en situaciones de herencia.
        self._sueldo_basico = valor

    def aumentar_sueldo(self, porcentaje):
        # El porcentaje debe ser mayor que cero.
        if porcentaje <= 0:
            raise ValueError("El porcentaje debe ser positivo")

        # Ejemplo:
        # sueldo = 50000
        # porcentaje = 10
        #
        # 1 + 10 / 100 = 1.10
        # 50000 * 1.10 = 55000
        self._sueldo_basico *= 1 + porcentaje / 100


# ---------------------------------------------------------------
# CASO 1: creación válida
# ---------------------------------------------------------------

empleado = Empleado("Ana", 50000)

print(f"${empleado.sueldo_basico:.2f}")  # $50000.00


# ---------------------------------------------------------------
# CASO 2: aumento válido
# ---------------------------------------------------------------

empleado.aumentar_sueldo(10)

print(f"${empleado.sueldo_basico:.2f}")  # $55000.00


# ---------------------------------------------------------------
# CASO 3: intento de asignar un sueldo negativo
#
# empleado.sueldo_basico = -1000
#         ↓
# setter
#         ↓
# -1000 < 0
#         ↓
# ValueError
# ---------------------------------------------------------------

try:
    empleado.sueldo_basico = -1000
except ValueError as error:
    print(f"Error: {error}")


# El sueldo anterior no fue modificado porque el valor inválido fue
# rechazado antes de llegar a self._sueldo_basico = valor.
print(f"${empleado.sueldo_basico:.2f}")  # $55000.00


# ---------------------------------------------------------------
# CASO 4: aumento con porcentaje inválido
#
# aumentar_sueldo(0)
#         ↓
# 0 <= 0
#         ↓
# ValueError
# ---------------------------------------------------------------

try:
    empleado.aumentar_sueldo(0)
except ValueError as error:
    print(f"Error: {error}")


# ---------------------------------------------------------------
# CASO 5: creación con sueldo inválido
#
# Empleado("Juan", -5000)
#         ↓
# __init__()
#         ↓
# setter
#         ↓
# sueldo negativo
#         ↓
# ValueError
# ---------------------------------------------------------------

try:
    empleado_invalido = Empleado("Juan", -5000)
except ValueError as error:
    print(f"Error: {error}")
