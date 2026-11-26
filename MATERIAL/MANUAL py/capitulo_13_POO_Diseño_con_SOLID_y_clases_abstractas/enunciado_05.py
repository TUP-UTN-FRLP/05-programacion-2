# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Type hints: escribí una clase Biblioteca completamente anotada, con
# nombre y una lista de Libro. Ojo con dos cosas que ya vimos: un libro
# es un objeto con identidad, no un diccionario suelto, y buscar_por_isbn
# lanza excepción si no encuentra, en vez de devolver None.
# -------------------------------------------------------------------------

class LibroNoEncontrado(Exception):
    """Indica que no existe un libro con ese ISBN."""

    pass


class Libro:
    """Libro con ISBN, título y autor."""

    def __init__(self, isbn: str, titulo: str, autor: str) -> None:
        self._isbn = isbn
        self._titulo = titulo
        self._autor = autor

    def isbn(self) -> str:
        """Devuelve el ISBN del libro."""
        return self._isbn

    def __str__(self) -> str:
        return f"'{self._titulo}' de {self._autor}"


class Biblioteca:
    """Biblioteca con anotaciones de tipo en toda su interfaz."""

    def __init__(self, nombre: str) -> None:
        self._nombre: str = nombre
        self._libros: dict[str, Libro] = {}

    def agregar_libro(self, libro: Libro) -> None:
        """Suma un libro al catálogo."""
        self._libros[libro.isbn()] = libro

    def buscar_por_isbn(self, isbn: str) -> Libro:
        """Devuelve el libro pedido o lanza excepción."""
        libro = self._libros.get(isbn)

        if libro is None:
            raise LibroNoEncontrado(f"No hay libro con ISBN {isbn}")

        return libro

    def cantidad_libros(self) -> int:
        """Cuántos libros hay en el catálogo."""
        return len(self._libros)

    def listar(self) -> list[Libro]:
        """Devuelve todos los libros del catálogo."""
        return list(self._libros.values())


if __name__ == "__main__":
    # list[Libro] y dict[str, Libro] requieren Python 3.9 o superior.
    biblioteca = Biblioteca("Biblioteca Central")
    biblioteca.agregar_libro(Libro("978-1", "El Aleph", "Borges"))
    biblioteca.agregar_libro(Libro("978-2", "Rayuela", "Cortázar"))

    print(biblioteca.buscar_por_isbn("978-1"))
    print(f"Total: {biblioteca.cantidad_libros()}")

    try:
        biblioteca.buscar_por_isbn("978-9")
    except LibroNoEncontrado as error:
        print(f"Error: {error}")
