# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# SRP: refactorizá una clase Empleado que representa nombre y sueldo,
# calcula el impuesto a las ganancias, imprime el recibo y se guarda a
# sí misma en una base de datos. Separá las cuatro responsabilidades y
# hacé que el repositorio sea usable de verdad, sin SQL de mentira.
# -------------------------------------------------------------------------

class Empleado:
    """Representa únicamente los datos de un empleado."""

    def __init__(self, legajo, nombre, sueldo):
        self._legajo = legajo
        self._nombre = nombre
        self._sueldo = sueldo

    def legajo(self):
        """Devuelve el legajo del empleado."""
        return self._legajo

    def nombre(self):
        """Devuelve el nombre del empleado."""
        return self._nombre

    def sueldo(self):
        """Devuelve el sueldo bruto."""
        return self._sueldo


class CalculadorGanancias:
    """Única responsabilidad: calcular el impuesto."""

    def __init__(self, alicuota=0.15):
        self._alicuota = alicuota

    def calcular(self, empleado):
        """Devuelve el impuesto que le corresponde al empleado."""
        return empleado.sueldo() * self._alicuota


class GeneradorRecibos:
    """Única responsabilidad: imprimir recibos."""

    def __init__(self, calculador):
        self._calculador = calculador

    def imprimir(self, empleado):
        """Imprime el recibo de sueldo del empleado."""
        impuesto = self._calculador.calcular(empleado)
        neto = empleado.sueldo() - impuesto

        print(f"Recibo de {empleado.nombre()}")
        print(f"  Bruto:    ${empleado.sueldo():.2f}")
        print(f"  Impuesto: ${impuesto:.2f}")
        print(f"  Neto:     ${neto:.2f}")


class RepositorioEmpleados:
    """Única responsabilidad: guardar y recuperar empleados."""

    def __init__(self):
        self._empleados = {}

    def guardar(self, empleado):
        """Persiste el empleado indexado por legajo."""
        self._empleados[empleado.legajo()] = empleado

    def obtener(self, legajo):
        """Devuelve el empleado o None si no está guardado."""
        return self._empleados.get(legajo)


if __name__ == "__main__":
    # Cuatro clases, cuatro razones para cambiar bien separadas. Si
    # mañana cambia la alícuota, se toca solo CalculadorGanancias.
    empleado = Empleado("E-1", "Ana", 800000)

    calculador = CalculadorGanancias()
    GeneradorRecibos(calculador).imprimir(empleado)

    repositorio = RepositorioEmpleados()
    repositorio.guardar(empleado)
    print(repositorio.obtener("E-1").nombre())
