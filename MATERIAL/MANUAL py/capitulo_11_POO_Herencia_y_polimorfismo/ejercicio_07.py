# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Creá las clases Pato, Robot y Alarma, sin relación de herencia entre
# sí. Cada una debe tener un método hablar() que devuelva un mensaje
# propio. Hacé una función hacer_hablar(cosa) que imprima cosa.hablar()
# y probala con objetos de las tres clases: eso es duck typing.
# -------------------------------------------------------------------------

class Pato:
    """Objeto que sabe hablar sin heredar de una clase común."""

    def hablar(self):
        """Devuelve el sonido del pato."""
        return "Cuac"


class Robot:
    """Objeto que sabe hablar sin heredar de una clase común."""

    def hablar(self):
        """Devuelve el mensaje binario del robot."""
        return "01001000..."


class Alarma:
    """Objeto que sabe hablar sin heredar de una clase común."""

    def hablar(self):
        """Devuelve el aviso de la alarma."""
        return "BEEP BEEP BEEP"


def hacer_hablar(cosa):
    """Invoca hablar() sin comprobar el tipo del objeto."""
    print(cosa.hablar())


hacer_hablar(Pato())
hacer_hablar(Robot())
hacer_hablar(Alarma())
