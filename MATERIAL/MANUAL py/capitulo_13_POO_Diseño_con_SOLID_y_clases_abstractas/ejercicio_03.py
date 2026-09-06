# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ¿Esta jerarquía viola LSP? Justificá. ArchivoLectura.leer() devuelve
# una cadena, y ArchivoEscritura hereda de ArchivoLectura pero
# sobrescribe leer() para lanzar PermissionError, además de agregar
# escribir(). Reorganizala si hace falta.
# -------------------------------------------------------------------------

class Archivo:
    """Base neutra: no promete ni lectura ni escritura."""

    def __init__(self, ruta):
        self._ruta = ruta

    def ruta(self):
        """Devuelve la ruta del archivo."""
        return self._ruta


class ArchivoLectura(Archivo):
    """Archivo que solo ofrece la operación de lectura."""

    def leer(self):
        """Devuelve el contenido del archivo."""
        return f"contenido de {self._ruta}"


class ArchivoEscritura(Archivo):
    """Archivo que solo ofrece la operación de escritura."""

    def escribir(self, contenido):
        """Guarda el contenido en el archivo."""
        print(f"Escribiendo en {self._ruta}: {contenido}")


if __name__ == "__main__":
    # Sí, la jerarquía original viola LSP: el padre promete que leer()
    # devuelve una cadena y la hija lanza PermissionError. Cualquier
    # código que reciba un ArchivoLectura se rompe al recibir un
    # ArchivoEscritura. Con una base neutra, ninguna promete algo que
    # la otra no pueda cumplir.
    print(ArchivoLectura("datos.txt").leer())
    ArchivoEscritura("salida.txt").escribir("hola")
