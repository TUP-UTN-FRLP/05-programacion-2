# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Persona con nombre, apellido y dni privados. Validá en
# el __init__: nombre y apellido no vacíos, DNI de 7 u 8 dígitos
# numéricos. Property nombre_completo de solo lectura que devuelva
# "Apellido, Nombre".
# -------------------------------------------------------------------------


class Persona:
    def __init__(self, nombre, apellido, dni):
        if not nombre.strip():
            raise ValueError("Nombre vacío")

        if not apellido.strip():
            raise ValueError("Apellido vacío")

        if not (
            isinstance(dni, str)
            and dni.isdigit()
            and len(dni) in (7, 8)
        ):
            raise ValueError(
                "DNI debe ser 7 u 8 dígitos numéricos"
            )

        self._nombre = nombre.strip().title()
        self._apellido = apellido.strip().title()
        self._dni = dni

    @property
    def nombre(self):
        return self._nombre

    @property
    def apellido(self):
        return self._apellido

    @property
    def dni(self):
        return self._dni

    @property
    def nombre_completo(self):
        return f"{self._apellido}, {self._nombre}"

    def __str__(self):
        return f"{self.nombre_completo} (DNI {self._dni})"


p = Persona("ana", "pérez", "12345678")

print(p.nombre_completo)  # Pérez, Ana

print(p)  # Pérez, Ana (DNI 12345678)

Persona("ana", "pérez", "abc")  # ValueError

Persona("ana", "pérez", "123")  # ValueError
