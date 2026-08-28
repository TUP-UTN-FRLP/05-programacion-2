# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Estudiante con nombre (privado, solo lectura) y una
# lista privada _notas. Métodos: agregar_nota(nota) que valide que la
# nota esté entre 0 y 10, promedio como property de solo lectura.
# -------------------------------------------------------------------------


class Estudiante:
    def __init__(self, nombre):
        self._nombre = nombre
        self._notas = []

    @property
    def nombre(self):
        return self._nombre

    def agregar_nota(self, nota):
        if not 0 <= nota <= 10:
            raise ValueError("La nota debe estar entre 0 y 10")

        self._notas.append(nota)

    @property
    def promedio(self):
        if not self._notas:
            return 0

        return sum(self._notas) / len(self._notas)


ana = Estudiante("Ana")

ana.agregar_nota(8)
ana.agregar_nota(9)

print(ana.promedio)  # 8.5
