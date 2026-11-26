# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 18
# Sumale a Estudiante un método mejor_nota() y un método esta_aprobado()
# (promedio >= 6).
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

    def mejor_nota(self):
        if len(self.notas) == 0:
            return None

        return max(self.notas)

    def esta_aprobado(self):
        return self.promedio() >= 6


ana = Estudiante("Ana")

ana.agregar_nota(8)
ana.agregar_nota(9)
ana.agregar_nota(7)

print(f"Mejor nota: {ana.mejor_nota()}")
print(f"Aprobado: {ana.esta_aprobado()}")
