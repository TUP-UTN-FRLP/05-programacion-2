# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Libro con titulo y autor, y un __str__ que devuelva
# "Titulo, de Autor". Después hacé LibroDigital(Libro) que agregue el
# formato y sobrescriba __str__ reutilizando el del padre con
# super().__str__(), en vez de repetir el formato completo.
# -------------------------------------------------------------------------

class Libro:
    """Libro impreso con título y autor."""

    def __init__(self, titulo, autor):
        self._titulo = titulo
        self._autor = autor

    def __str__(self):
        return f"{self._titulo}, de {self._autor}"


class LibroDigital(Libro):
    """Libro que además tiene un formato de archivo."""

    def __init__(self, titulo, autor, formato):
        super().__init__(titulo, autor)
        self._formato = formato

    def __str__(self):
        return f"{super().__str__()} [{self._formato}]"


papel = Libro("Rayuela", "Cortázar")
digital = LibroDigital("El Aleph", "Borges", "PDF")

print(papel)
print(digital)
