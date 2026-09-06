# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Motor con cilindrada y potencia, y una clase Auto con
# marca, modelo y un Motor. Imprimí un auto con toda su información.
# Después creá un solo Motor y dos Autos que lo compartan, cambiale la
# potencia y observá que los dos autos ven el cambio: guardan una
# referencia al mismo objeto, no una copia. Pensá por qué compartir un
# motor entre dos autos es un error de modelado.
# -------------------------------------------------------------------------

class Motor:
    """Motor de un auto. En la realidad pertenece a un solo auto."""

    def __init__(self, cilindrada, potencia):
        self._cilindrada = cilindrada
        self._potencia = potencia

    def ajustar_potencia(self, potencia):
        """Cambia la potencia declarada del motor."""
        self._potencia = potencia

    def __str__(self):
        return f"Motor {self._cilindrada}cc / {self._potencia}HP"


class Auto:
    """Auto compuesto por un objeto Motor."""

    def __init__(self, marca, modelo, motor):
        self._marca = marca
        self._modelo = modelo
        self._motor = motor

    def __str__(self):
        return f"{self._marca} {self._modelo} - {self._motor}"


if __name__ == "__main__":
    auto = Auto("Ford", "Focus", Motor(2000, 150))
    print(auto)

    # Un mismo motor referenciado por dos autos.
    compartido = Motor(1600, 110)
    uno = Auto("Fiat", "Cronos", compartido)
    otro = Auto("Peugeot", "208", compartido)

    compartido.ajustar_potencia(120)

    print(uno)
    print(otro)

    # Los dos cambiaron: es un solo Motor con dos referencias.
    # Con una Direccion compartida entre dos Personas esto sería
    # correcto (agregación). Con un Motor no lo es: un motor
    # pertenece a un único auto y debería crearse para él.
