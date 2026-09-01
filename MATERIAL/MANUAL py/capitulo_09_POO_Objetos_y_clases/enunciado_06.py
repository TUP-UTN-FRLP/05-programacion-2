# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 06
# Sumale a Libro un método es_extenso() que devuelva True si tiene más
# de 300 páginas.
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

    def es_extenso(self):
        return self.paginas > 300


corto = Libro("El Aleph", "Borges", 224)
largo = Libro("Rayuela", "Cortázar", 736)

print(f"{corto.titulo} extenso? {corto.es_extenso()}")
print(f"{largo.titulo} extenso? {largo.es_extenso()}")
