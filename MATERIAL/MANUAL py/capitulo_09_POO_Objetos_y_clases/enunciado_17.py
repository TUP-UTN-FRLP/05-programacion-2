# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 17
# Definí una clase Estudiante con nombre y una lista de notas (que
# arranca vacía). Agregale un método agregar_nota(nota) y un método
# promedio().
# -------------------------------------------------------------------------


class Estudiante:

    def __init__(self, nombre):
        self.nombre = nombre
        self.notas = []

    def agregar_nota(self, nota):
        self.notas.append(nota)

    def promedio(self):
        if len(self.notas) == 0:
            return 0

        return sum(self.notas) / len(self.notas)


ana = Estudiante("Ana")

ana.agregar_nota(8)
ana.agregar_nota(9)
ana.agregar_nota(7)

print(f"Promedio de {ana.nombre}: {ana.promedio():.2f}")
