from validaciones_2 import validar_limite_extraccion


class Cajero:
    def __init__(self, limite):
        self.__limite = validar_limite_extraccion(limite)

    @property
    def limite(self):
        return self.__limite


cajero = Cajero(100000)
print(cajero.limite)

# Cajero(0)
