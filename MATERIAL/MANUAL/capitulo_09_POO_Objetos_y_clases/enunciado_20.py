# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 20
# Definí una clase Cronometro con atributos horas, minutos y segundos
# (todos arrancan en 0). Agregale un método avanzar_segundo() que suma
# 1 al segundero, y cuando llega a 60 pasa a los minutos, y cuando los
# minutos llegan a 60 pasa a las horas. Agregale un __str__ que muestre
# "01:23:45".
# -------------------------------------------------------------------------


class Cronometro:

    def __init__(self):
        self.horas = 0
        self.minutos = 0
        self.segundos = 0

    def avanzar_segundo(self):
        self.segundos += 1

        if self.segundos == 60:
            self.segundos = 0
            self.minutos += 1

            if self.minutos == 60:
                self.minutos = 0
                self.horas += 1

    def __str__(self):
        return (
            f"{self.horas}:"
            f"{self.minutos:02d}:"
            f"{self.segundos:02d}"
        )


c = Cronometro()

for _ in range(3700):
    c.avanzar_segundo()
    print(c)
