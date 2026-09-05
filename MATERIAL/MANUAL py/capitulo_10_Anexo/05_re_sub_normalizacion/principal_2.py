from validaciones_2 import validar_domicilio


class Cliente:
    def __init__(self, domicilio):
        self.__domicilio = validar_domicilio(domicilio)

    @property
    def domicilio(self):
        return self.__domicilio


cliente = Cliente("  Calle   50    1234 ")
print(cliente.domicilio)

# Caso invalido:
# Cliente("   ")

