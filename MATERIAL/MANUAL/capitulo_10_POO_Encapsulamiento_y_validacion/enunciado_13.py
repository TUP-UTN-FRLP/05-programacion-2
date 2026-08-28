# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Sumale a Semaforo un método cambiar() que rote el estado según la
# lógica: verde - amarillo - rojo - verde.
# -------------------------------------------------------------------------


class Semaforo:
    def __init__(self):
        self._estado = "rojo"

    @property
    def estado(self):
        return self._estado

    @estado.setter
    def estado(self, valor):
        if valor not in ("rojo", "amarillo", "verde"):
            raise ValueError(f"Estado inválido: {valor}")

        self._estado = valor

    def cambiar(self):
        transiciones = {
            "verde": "amarillo",
            "amarillo": "rojo",
            "rojo": "verde",
        }

        self._estado = transiciones[self._estado]


s = Semaforo()

print(s.estado)  # rojo

s.cambiar()
print(s.estado)  # verde

s.cambiar()
print(s.estado)  # amarillo

s.cambiar()
print(s.estado)  # rojo
