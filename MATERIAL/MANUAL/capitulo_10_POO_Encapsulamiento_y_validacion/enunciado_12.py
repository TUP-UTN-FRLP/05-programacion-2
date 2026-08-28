# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Semaforo con _estado privado (valores válidos: "rojo",
# "amarillo", "verde"). El setter debe rechazar cualquier otro valor.
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


s = Semaforo()

s.estado = "verde"  # OK

s.estado = "azul"  # ValueError
