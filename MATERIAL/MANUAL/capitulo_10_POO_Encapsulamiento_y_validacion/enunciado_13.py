# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Sumale a Semaforo un método cambiar() que rote el estado según la
# lógica: verde - amarillo - rojo - verde.
# -------------------------------------------------------------------------


class Semaforo:
    def __init__(self):
        # El semáforo comienza siempre en rojo.
        #
        # _estado es el atributo interno donde se guarda el estado.
        # Usamos un solo guion bajo porque en Python indica, por
        # convención, que el atributo es de uso interno de la clase.
        # Técnicamente puede accederse desde afuera, pero hacerlo
        # significa romper el contrato de la clase.
        #
        # No usamos __estado porque el doble guion bajo activa name
        # mangling, usado principalmente para evitar colisiones de
        # nombres en situaciones de herencia.
        self._estado = "rojo"

    @property
    def estado(self):
        # estado es la property pública que permite consultar _estado.
        return self._estado

    @estado.setter
    def estado(self, valor):
        # El setter controla que solamente puedan asignarse estados
        # válidos.
        #
        # Secuencia:
        # semaforo.estado = valor
        #         ↓
        # setter de estado
        #         ↓
        # validar el valor
        #         ↓
        # self._estado = valor
        if valor not in ("rojo", "amarillo", "verde"):
            raise ValueError(f"Estado inválido: {valor}")

        self._estado = valor

    def cambiar(self):
        # El diccionario representa las transiciones posibles.
        #
        # La clave es el estado actual y el valor indica cuál debe ser
        # el siguiente estado.
        #
        # "rojo"     → "verde"
        # "verde"    → "amarillo"
        # "amarillo" → "rojo"
        transiciones = {
            "verde": "amarillo",
            "amarillo": "rojo",
            "rojo": "verde",
        }

        # Primero buscamos el siguiente estado usando el estado actual
        # como clave del diccionario.
        siguiente_estado = transiciones[self._estado]

        # No modificamos directamente:
        # self._estado = siguiente_estado
        #
        # Usamos la property para que el cambio pase también por el
        # setter y mantengamos una única puerta de entrada al atributo.
        self.estado = siguiente_estado


# ---------------------------------------------------------------
# CASO 1: creación del semáforo
#
# Semaforo()
#       ↓
# __init__()
#       ↓
# _estado = "rojo"
# ---------------------------------------------------------------

semaforo = Semaforo()

print(semaforo.estado)  # rojo


# ---------------------------------------------------------------
# CASO 2: primer cambio
#
# estado actual: "rojo"
#       ↓
# transiciones["rojo"]
#       ↓
# "verde"
#       ↓
# self.estado = "verde"
#       ↓
# setter
#       ↓
# _estado = "verde"
# ---------------------------------------------------------------

semaforo.cambiar()

print(semaforo.estado)  # verde


# ---------------------------------------------------------------
# CASO 3: segundo cambio
#
# "verde" → "amarillo"
# ---------------------------------------------------------------

semaforo.cambiar()

print(semaforo.estado)  # amarillo


# ---------------------------------------------------------------
# CASO 4: tercer cambio
#
# "amarillo" → "rojo"
#
# Después de tres cambios volvemos al estado inicial.
# ---------------------------------------------------------------

semaforo.cambiar()

print(semaforo.estado)  # rojo


# ---------------------------------------------------------------
# CASO 5: comienza un nuevo ciclo
#
# "rojo" → "verde"
# ---------------------------------------------------------------

semaforo.cambiar()

print(semaforo.estado)  # verde


# ---------------------------------------------------------------
# CASO 6: intento de asignar un estado inválido desde afuera
#
# semaforo.estado = "azul"
#       ↓
# setter
#       ↓
# "azul" no es un estado válido
#       ↓
# ValueError
# ---------------------------------------------------------------

try:
    semaforo.estado = "azul"
except ValueError as error:
    print(f"Error: {error}")


# Como el valor inválido fue rechazado, se conserva el estado anterior.
print(semaforo.estado)  # verde
