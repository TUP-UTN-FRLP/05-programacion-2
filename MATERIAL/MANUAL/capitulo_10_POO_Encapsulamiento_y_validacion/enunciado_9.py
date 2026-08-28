# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Sumale a Estudiante una property mejor_nota (solo lectura) y un método
# borrar_ultima_nota() que devuelva la nota borrada, o lance IndexError
# si no hay notas.
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

    @property
    def mejor_nota(self):
        if not self._notas:
            return None

        return max(self._notas)

    def borrar_ultima_nota(self):
        if not self._notas:
            raise IndexError("No hay notas para borrar")

        return self._notas.pop()


ana = Estudiante("Ana")

ana.agregar_nota(8)
ana.agregar_nota(9)

print(ana.mejor_nota)  # 9
print(ana.borrar_ultima_nota())  # 9 (la que sacamos)
print(ana.promedio)  # 8.0 (solo queda la 8)
