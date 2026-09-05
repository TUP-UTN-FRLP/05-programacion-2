from validaciones_1 import validar_nombre


class Titular:
    def __init__(self, nombre):
        self.__nombre = validar_nombre(nombre)

    @property
    def nombre(self):
        return self.__nombre


titular = Titular("Ana María")
print(titular.nombre)

# Titular("Ana_123")
