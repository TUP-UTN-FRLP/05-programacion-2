# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# SRP: te dan una clase Biblioteca que gestiona libros, los imprime por
# pantalla y además los exporta a CSV. Son tres razones distintas para
# cambiarla. Partila en tres clases: Biblioteca, que solo administra la
# colección; MostradorDeLibros, que sabe imprimir; y ExportadorCsv, que
# sabe armar el texto CSV. Fijate que ninguna de las tres necesita
# conocer el trabajo de las otras dos.
# -------------------------------------------------------------------------

class Libro:
    """Libro con título, autor e ISBN."""

    def __init__(self, isbn, titulo, autor):
        self._isbn = isbn
        self._titulo = titulo
        self._autor = autor

    def isbn(self):
        """Devuelve el ISBN del libro."""
        return self._isbn

    def titulo(self):
        """Devuelve el título del libro."""
        return self._titulo

    def autor(self):
        """Devuelve el autor del libro."""
        return self._autor

    def __str__(self):
        return f"'{self._titulo}' de {self._autor}"


class Biblioteca:
    """Única responsabilidad: administrar la colección."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._libros = {}

    def nombre(self):
        """Devuelve el nombre de la biblioteca."""
        return self._nombre

    def agregar(self, libro):
        """Suma un libro al catálogo."""
        self._libros[libro.isbn()] = libro

    def listar(self):
        """Devuelve todos los libros del catálogo."""
        return list(self._libros.values())


class MostradorDeLibros:
    """Única responsabilidad: presentar libros por pantalla."""

    def mostrar(self, biblioteca):
        """Imprime el catálogo de una biblioteca."""
        print(f"{biblioteca.nombre()}")

        for libro in biblioteca.listar():
            print(f"  - {libro}")


class ExportadorCsv:
    """Única responsabilidad: representar libros como CSV."""

    def exportar(self, biblioteca):
        """Devuelve el catálogo como texto CSV."""
        lineas = ["isbn,titulo,autor"]

        for libro in biblioteca.listar():
            lineas.append(
                f"{libro.isbn()},{libro.titulo()},"
                f"{libro.autor()}"
            )

        return "\n".join(lineas)


if __name__ == "__main__":
    biblioteca = Biblioteca("Biblioteca Central")
    biblioteca.agregar(
        Libro("978-987-1", "El Aleph", "Borges")
    )
    biblioteca.agregar(
        Libro("978-987-2", "Rayuela", "Cortázar")
    )

    MostradorDeLibros().mostrar(biblioteca)

    print()
    print(ExportadorCsv().exportar(biblioteca))
