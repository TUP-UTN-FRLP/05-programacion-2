from validaciones_2 import validar_numero_cuenta


class Cuenta:
    def __init__(self, numero):
        self.__numero = validar_numero_cuenta(numero)

    @property
    def numero(self):
        return self.__numero


cuenta = Cuenta("12345678901234")
print(cuenta.numero)
