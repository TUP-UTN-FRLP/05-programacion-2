# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Semaforo con _estado privado (valores válidos: "rojo",
# "amarillo", "verde"). El setter debe rechazar cualquier otro valor.
# -------------------------------------------------------------------------


class Semaforo:
    def __init__(self):
        # El semáforo comienza siempre en rojo.
        #
        # En este caso asignamos directamente a _estado porque "rojo" es
        # un valor conocido y válido definido por la propia clase.
        #
        # Usamos un solo guion bajo (_estado) porque en Python indica,
        # por convención, que el atributo es de uso interno de la clase.
        # Técnicamente puede accederse desde afuera, pero hacerlo
        # significa romper el contrato de la clase.
        #
        # No usamos __estado porque el doble guion bajo activa name
        # mangling, usado principalmente para evitar colisiones de
        # nombres en situaciones de herencia.
        self._estado = "rojo"

    @property
    def estado(self):
        # estado es la property pública.
        # _estado es el atributo interno donde se guarda el valor.
        return self._estado

    @estado.setter
    def estado(self, valor):
        # Este setter se ejecuta automáticamente cuando hacemos:
        # semaforo.estado = valor
        #
        # Secuencia:
        # semaforo.estado = valor
        #         ↓
        # setter de estado
        #         ↓
        # verificar que el valor sea válido
        #         ↓
        # self._estado = valor
        if valor not in ("rojo", "amarillo", "verde"):
            raise ValueError(f"Estado inválido: {valor}")

        # El nuevo estado se guarda solamente después de superar la
        # validación.
        self._estado = valor


# ---------------------------------------------------------------
# CASO 1: creación del semáforo
#
# Semaforo()
#       ↓
# __init__()
#       ↓
# self._estado = "rojo"
# ---------------------------------------------------------------

semaforo = Semaforo()

print(semaforo.estado)  # rojo


# ---------------------------------------------------------------
# CASO 2: cambio a un estado válido
#
# semaforo.estado = "verde"
#       ↓
# setter
#       ↓
# "verde" pertenece a los estados permitidos
#       ↓
# self._estado = "verde"
# ---------------------------------------------------------------

semaforo.estado = "verde"

print(semaforo.estado)  # verde


# ---------------------------------------------------------------
# CASO 3: otro cambio válido
# ---------------------------------------------------------------

semaforo.estado = "amarillo"

print(semaforo.estado)  # amarillo


# ---------------------------------------------------------------
# CASO 4: intento de asignar un estado inválido
#
# semaforo.estado = "azul"
#       ↓
# setter
#       ↓
# "azul" no pertenece a los estados permitidos
#       ↓
# ValueError
# ---------------------------------------------------------------

try:
    semaforo.estado = "azul"
except ValueError as error:
    print(f"Error: {error}")


# Como el valor inválido fue rechazado, el estado anterior se conserva.
print(semaforo.estado)  # amarillo
