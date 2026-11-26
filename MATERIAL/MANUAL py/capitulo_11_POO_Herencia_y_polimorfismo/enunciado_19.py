# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Creá tres clases sin relación de herencia entre sí: Sensor, Reloj y
# Termostato. Cada una implementa leer(), que devuelve una cadena con su
# lectura actual. Escribí una función informar(dispositivos) que recorra
# cualquier lista y llame leer() sobre cada elemento. Esto es duck
# typing: no hay un padre común, alcanza con que el método exista.
#
# Ojo: hacer lo mismo con __str__ no sería duck typing puro, porque
# __str__ ya viene definido en object y toda clase lo hereda.
# -------------------------------------------------------------------------

class Sensor:
    """Dispositivo que informa una temperatura medida."""

    def __init__(self, ubicacion, temperatura):
        self._ubicacion = ubicacion
        self._temperatura = temperatura

    def leer(self):
        """Devuelve la lectura del sensor como texto."""
        return f"Sensor {self._ubicacion}: {self._temperatura} C"


class Reloj:
    """Dispositivo que informa una hora."""

    def __init__(self, hora, minuto):
        self._hora = hora
        self._minuto = minuto

    def leer(self):
        """Devuelve la hora como texto."""
        return f"Reloj: {self._hora:02d}:{self._minuto:02d}"


class Termostato:
    """Dispositivo que informa la temperatura configurada."""

    def __init__(self, objetivo):
        self._objetivo = objetivo

    def leer(self):
        """Devuelve la consigna del termostato como texto."""
        return f"Termostato: consigna {self._objetivo} C"


def informar(dispositivos):
    """Muestra la lectura de cualquier objeto que sepa leer()."""
    for dispositivo in dispositivos:
        print(dispositivo.leer())


tablero = [
    Sensor("cocina", 22),
    Reloj(9, 5),
    Termostato(24),
    Sensor("patio", 17),
]

informar(tablero)
