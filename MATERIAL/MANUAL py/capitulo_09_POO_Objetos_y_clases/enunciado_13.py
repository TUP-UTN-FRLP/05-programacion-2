# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 13
# Definí una clase Fecha con atributos dia, mes y anio. Agregale un
# __str__ que muestre "25/07/2026", con ceros a la izquierda para día
# y mes.
# -------------------------------------------------------------------------


class Fecha:

    def __init__(self, dia, mes, anio):
        self.dia = dia
        self.mes = mes
        self.anio = anio

    def __str__(self):
        return f"{self.dia:02d}/{self.mes:02d}/{self.anio}"


f = Fecha(5, 7, 2026)

print(f)

f2 = Fecha(25, 12, 2026)

print(f2)
