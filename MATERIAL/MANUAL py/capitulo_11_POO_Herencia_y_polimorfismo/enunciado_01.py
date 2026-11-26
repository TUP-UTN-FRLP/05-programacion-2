# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Definí una clase Vehiculo con atributos marca y modelo, y un método
# descripcion() que los imprima. Después definí Moto(Vehiculo) con un
# atributo extra cilindrada. Usá super() en el __init__. Sobrescribí
# descripcion() para que llame a la del padre y agregue la cilindrada.
# -------------------------------------------------------------------------

class Vehiculo:
    """Vehículo con marca y modelo."""

    def __init__(self, marca, modelo):
        self._marca = marca
        self._modelo = modelo

    def descripcion(self):
        """Imprime los datos comunes a todo vehículo."""
        print(f"{self._marca} {self._modelo}")


class Moto(Vehiculo):
    """Moto que agrega la cilindrada al vehículo base."""

    def __init__(self, marca, modelo, cilindrada):
        super().__init__(marca, modelo)
        self._cilindrada = cilindrada

    def descripcion(self):
        """Extiende la descripción del padre con la cilindrada."""
        super().descripcion()
        print(f"Cilindrada: {self._cilindrada}cc")


vehiculo = Vehiculo("Ford", "Focus")
moto = Moto("Honda", "CBR", 600)

vehiculo.descripcion()
print()
moto.descripcion()
