# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 19
# Definí una clase Contador con atributo valor que arranca en 0.
# Agregale métodos incrementar(), decrementar() y reiniciar().
# -------------------------------------------------------------------------


class Contador:

    def __init__(self):
        self.valor = 0

    def incrementar(self):
        self.valor += 1

    def decrementar(self):
        self.valor -= 1

    def reiniciar(self):
        self.valor = 0

    def __str__(self):
        return f"Contador: {self.valor}"


c = Contador()

c.incrementar()
c.incrementar()
c.incrementar()

print(c)

c.decrementar()

print(c)

c.reiniciar()

print(c)
