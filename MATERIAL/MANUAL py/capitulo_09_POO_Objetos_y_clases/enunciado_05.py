# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 05
# Definí una clase Libro con atributos titulo, autor y paginas.
# Agregale un __str__ que devuelva "'Título' de Autor (N páginas)".
# -------------------------------------------------------------------------


class Libro:

    def __init__(self, titulo, autor, paginas):
        self.titulo = titulo
        self.autor = autor
        self.paginas = paginas

    def __str__(self):
        return (
            f"'{self.titulo}' de {self.autor} "
            f"({self.paginas} páginas)"
        )


libro = Libro("El Aleph", "Jorge Luis Borges", 224)

print(libro)
