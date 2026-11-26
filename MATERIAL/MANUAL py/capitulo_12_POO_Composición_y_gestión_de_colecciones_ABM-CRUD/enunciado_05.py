# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Playlist con nombre y una lista de Cancion. Cada
# Cancion tiene titulo, artista y duracion_seg. Agregá los métodos
# agregar_cancion(), duracion_total(), cantidad() y listar(). Mostrá
# la duración total en formato minutos:segundos.
# -------------------------------------------------------------------------

class Cancion:
    """Canción con título, artista y duración en segundos."""

    def __init__(self, titulo, artista, duracion_seg):
        self._titulo = titulo
        self._artista = artista
        self._duracion_seg = duracion_seg

    def duracion_seg(self):
        """Devuelve la duración de la canción en segundos."""
        return self._duracion_seg

    def __str__(self):
        minutos, segundos = divmod(self._duracion_seg, 60)
        return (
            f"{self._titulo} - {self._artista} "
            f"({minutos}:{segundos:02d})"
        )


class Playlist:
    """Playlist que contiene una colección de canciones."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._canciones = []

    def agregar_cancion(self, cancion):
        """Suma una canción al final de la playlist."""
        self._canciones.append(cancion)

    def cantidad(self):
        """Devuelve cuántas canciones tiene la playlist."""
        return len(self._canciones)

    def duracion_total(self):
        """Suma las duraciones de todas las canciones."""
        return sum(
            cancion.duracion_seg()
            for cancion in self._canciones
        )

    def listar(self):
        """Imprime el detalle de la playlist."""
        minutos, segundos = divmod(self.duracion_total(), 60)
        print(f"{self._nombre} ({self.cantidad()} temas)")

        for cancion in self._canciones:
            print(f"  {cancion}")

        print(f"  Duración total: {minutos}:{segundos:02d}")


if __name__ == "__main__":
    playlist = Playlist("Rock nacional")
    playlist.agregar_cancion(
        Cancion("Seminare", "Serú Girán", 315)
    )
    playlist.agregar_cancion(
        Cancion("Rasguña las piedras", "Sui Generis", 240)
    )

    playlist.listar()
