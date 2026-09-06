from validaciones_3 import validar_alias


class Cuenta:
    def __init__(self, alias):
        self.__alias = validar_alias(alias)

    @property
    def alias(self):
        return self.__alias


cuenta = Cuenta("sergio.123")
print(cuenta.alias)

# Caso invalido:
# Cuenta("1sergio")

