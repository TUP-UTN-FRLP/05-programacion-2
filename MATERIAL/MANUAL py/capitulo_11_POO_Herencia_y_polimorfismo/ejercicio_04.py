# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Hacé una clase Rectangulo con __init__(base, altura) y un método
# area() que devuelve base * altura. Después hacé Cuadrado(Rectangulo)
# con un solo parámetro lado en el constructor: usá super() para pasar
# el mismo valor como base y altura. Sobrescribí descripcion():
# Rectangulo imprime "Rectángulo de base X y altura Y" y Cuadrado,
# "Cuadrado de lado X". Fijate que area() no hace falta reescribirla.
# -------------------------------------------------------------------------

class Rectangulo:
    """Rectángulo definido por base y altura."""

    def __init__(self, base, altura):
        self._base = base
        self._altura = altura

    def area(self):
        """Devuelve base por altura."""
        return self._base * self._altura

    def descripcion(self):
        """Imprime las dos dimensiones del rectángulo."""
        print(
            f"Rectángulo de base {self._base} "
            f"y altura {self._altura}"
        )


class Cuadrado(Rectangulo):
    """Rectángulo especializado cuyos dos lados son iguales."""

    def __init__(self, lado):
        super().__init__(lado, lado)

    def descripcion(self):
        """Imprime el único lado que define al cuadrado."""
        print(f"Cuadrado de lado {self._base}")


rectangulo = Rectangulo(5, 3)
rectangulo.descripcion()
print(rectangulo.area())

cuadrado = Cuadrado(4)
cuadrado.descripcion()
print(cuadrado.area())
