# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Partí de una clase Empleado con __init__(nombre), que guarda el
# nombre, y un método presentarse() que imprime "Soy Ana". Hacé una
# hija Gerente que agrega el atributo equipo, la lista de personas a
# cargo. Su __init__ debe usar super() para no repetir código. Además,
# Gerente.presentarse() debe llamar a la del padre y agregar "y dirijo
# un equipo de N personas".
# -------------------------------------------------------------------------

class Empleado:
    """Empleado con nombre y presentación básica."""

    def __init__(self, nombre):
        self._nombre = nombre

    def presentarse(self):
        """Imprime la presentación común a todo empleado."""
        print(f"Soy {self._nombre}")


class Gerente(Empleado):
    """Empleado que además dirige un equipo."""

    def __init__(self, nombre, equipo):
        super().__init__(nombre)
        self._equipo = equipo

    def presentarse(self):
        """Extiende la presentación del padre con el equipo."""
        super().presentarse()
        print(f"y dirijo un equipo de {len(self._equipo)} personas")


empleado = Empleado("Juan")

gerente = Gerente("Ana", ["Juan", "Pedro", "Lucía"])

empleado.presentarse()
print()
gerente.presentarse()
