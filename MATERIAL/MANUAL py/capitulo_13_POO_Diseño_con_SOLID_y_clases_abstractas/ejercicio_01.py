# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Identificá por qué esta clase viola SRP y proponé cómo partirla.
# Alumno representa nombre y notas, calcula el promedio, se guarda a sí
# misma en un archivo y envía el boletín por email.
# -------------------------------------------------------------------------

class Alumno:
    """Representa un alumno y calcula su promedio. Nada más."""

    def __init__(self, nombre, notas):
        self._nombre = nombre
        self._notas = list(notas)

    def nombre(self):
        """Devuelve el nombre del alumno."""
        return self._nombre

    def notas(self):
        """Devuelve una copia de las notas."""
        return list(self._notas)

    def promedio(self):
        """Promedio de las notas; 0 si todavía no tiene ninguna."""
        if not self._notas:
            return 0

        return sum(self._notas) / len(self._notas)


class RepositorioAlumnos:
    """Única responsabilidad: guardar y cargar alumnos de disco."""

    def guardar(self, alumno, ruta):
        """Escribe el alumno en un archivo de texto."""
        with open(ruta, "w", encoding="utf-8") as archivo:
            archivo.write(f"{alumno.nombre()}: {alumno.notas()}")


class NotificadorEmail:
    """Única responsabilidad: enviar mensajes por email."""

    def enviar_boletin(self, alumno, email):
        """Simula el envío del boletín al alumno."""
        print(
            f"[EMAIL a {email}] {alumno.nombre()}, "
            f"promedio {alumno.promedio():.2f}"
        )


if __name__ == "__main__":
    # Tres razones para cambiar en la clase original: la definición de
    # alumno, el formato del archivo y el servidor de correo.
    alumno = Alumno("Ana", [8, 9, 7])

    print(f"{alumno.nombre()}: {alumno.promedio():.2f}")
    NotificadorEmail().enviar_boletin(alumno, "ana@correo.com")
