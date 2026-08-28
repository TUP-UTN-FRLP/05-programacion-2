# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Libro con titulo, autor y paginas, más un _leido
# privado (booleano, arranca en False) expuesto como property de solo
# lectura. Método marcar_como_leido() que lo pone en True, y
# desmarcar() que lo pone en False.
# -------------------------------------------------------------------------


class Libro:
    def __init__(self, titulo, autor, paginas):
        if not titulo.strip():
            raise ValueError("Título vacío")

        if paginas <= 0:
            raise ValueError("Debe tener al menos 1 página")

        self._titulo = titulo.strip()
        self._autor = autor.strip()
        self._paginas = paginas
        self._leido = False

    @property
    def leido(self):
        return self._leido

    def marcar_como_leido(self):
        self._leido = True

    def desmarcar(self):
        self._leido = False

    def __str__(self):
        estado = "leído" if self._leido else "sin leer"
        return f"'{self._titulo}' de {self._autor} ({estado})"


l = Libro("El Aleph", "Borges", 224)

print(l)  # 'El Aleph' de Borges (sin leer)

l.marcar_como_leido()

print(l)  # 'El Aleph' de Borges (leído)

l.leido = True  # AttributeError
