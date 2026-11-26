# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Vehiculo con marca y velocidad_maxima. Hacé
# Auto(Vehiculo) que agrega cantidad_puertas y después
# AutoDeportivo(Auto) que agrega caballos_de_fuerza. Cada nivel usa
# super() en el __init__ y sobrescribe __str__ reutilizando el del
# padre con super().__str__() para agregar solo su información extra.
# -------------------------------------------------------------------------

class Vehiculo:
    """Vehículo con marca y velocidad máxima."""

    def __init__(self, marca, velocidad_maxima):
        self._marca = marca
        self._velocidad_maxima = velocidad_maxima

    def __str__(self):
        return f"{self._marca} (Vmax: {self._velocidad_maxima}km/h)"


class Auto(Vehiculo):
    """Vehículo que agrega cantidad de puertas."""

    def __init__(self, marca, velocidad_maxima, cantidad_puertas):
        super().__init__(marca, velocidad_maxima)
        self._cantidad_puertas = cantidad_puertas

    def __str__(self):
        return f"{super().__str__()}, {self._cantidad_puertas} puertas"


class AutoDeportivo(Auto):
    """Auto que agrega caballos de fuerza."""

    def __init__(
        self,
        marca,
        velocidad_maxima,
        cantidad_puertas,
        caballos_de_fuerza,
    ):
        super().__init__(marca, velocidad_maxima, cantidad_puertas)
        self._caballos_de_fuerza = caballos_de_fuerza

    def __str__(self):
        return f"{super().__str__()}, {self._caballos_de_fuerza} HP"


vehiculos = [
    Vehiculo("Ford", 180),
    Auto("Toyota", 200, 4),
    AutoDeportivo("Ferrari", 320, 2, 720),
]

for vehiculo in vehiculos:
    print(vehiculo)
