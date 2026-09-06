from validaciones_1 import validar_saldo_inicial


class Cuenta:
    def __init__(self, saldo_inicial):
        self.__saldo = validar_saldo_inicial(saldo_inicial)

    @property
    def saldo(self):
        return self.__saldo


cuenta = Cuenta(5000)
print(cuenta.saldo)

# Cuenta(-1)
