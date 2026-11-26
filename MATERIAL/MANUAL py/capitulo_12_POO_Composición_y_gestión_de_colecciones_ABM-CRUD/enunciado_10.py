# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Empresa con una lista de Empleado. Cada Empleado tiene
# legajo, nombre, sueldo y departamento. Agregá contratar(),
# despedir(legajo), que lance excepción si el legajo no existe,
# promedio_sueldos() y empleados_por_departamento(depto). Usá el legajo
# como identificador, no el nombre: dos empleados pueden llamarse igual.
# -------------------------------------------------------------------------

class EmpleadoNoEncontrado(Exception):
    """Indica que no existe el empleado solicitado."""

    pass


class Empleado:
    """Empleado con legajo, sueldo y departamento."""

    def __init__(self, legajo, nombre, sueldo, departamento):
        self._legajo = legajo
        self._nombre = nombre
        self._sueldo = sueldo
        self._departamento = departamento

    def legajo(self):
        """Devuelve el legajo del empleado."""
        return self._legajo

    def sueldo(self):
        """Devuelve el sueldo del empleado."""
        return self._sueldo

    def departamento(self):
        """Devuelve el departamento del empleado."""
        return self._departamento

    def __str__(self):
        return (
            f"[{self._legajo}] {self._nombre} - "
            f"{self._departamento} (${self._sueldo})"
        )


class Empresa:
    """Empresa que administra una colección de empleados."""

    def __init__(self, nombre):
        self._nombre = nombre
        self._empleados = []

    def contratar(self, empleado):
        """Suma un empleado a la nómina."""
        self._empleados.append(empleado)

    def buscar_por_legajo(self, legajo):
        """Devuelve el empleado con ese legajo o lanza excepción."""
        for empleado in self._empleados:
            if empleado.legajo() == legajo:
                return empleado

        raise EmpleadoNoEncontrado(
            f"No hay empleado con legajo {legajo}"
        )

    def despedir(self, legajo):
        """Saca de la nómina al empleado indicado."""
        empleado = self.buscar_por_legajo(legajo)
        self._empleados.remove(empleado)

    def promedio_sueldos(self):
        """Promedio de sueldos; 0 si no hay empleados."""
        if not self._empleados:
            return 0

        total = sum(
            empleado.sueldo()
            for empleado in self._empleados
        )

        return total / len(self._empleados)

    def empleados_por_departamento(self, depto):
        """Devuelve los empleados de un departamento."""
        return [
            empleado
            for empleado in self._empleados
            if empleado.departamento() == depto
        ]


if __name__ == "__main__":
    empresa = Empresa("Sistemas SA")
    empresa.contratar(Empleado("E-1", "Ana", 500000, "IT"))
    empresa.contratar(Empleado("E-2", "Juan", 600000, "IT"))
    empresa.contratar(
        Empleado("E-3", "Pedro", 450000, "Ventas")
    )

    print(f"Promedio: ${empresa.promedio_sueldos():.2f}")

    for empleado in empresa.empleados_por_departamento("IT"):
        print(f"  {empleado}")

    empresa.despedir("E-2")

    try:
        empresa.despedir("E-99")
    except EmpleadoNoEncontrado as error:
        print(f"Error: {error}")
