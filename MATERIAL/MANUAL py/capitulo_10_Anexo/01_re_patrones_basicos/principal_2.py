from validaciones_2 import validar_usuario


class CuentaWeb:
    def __init__(self, usuario):
        self.__usuario = validar_usuario(usuario)

    @property
    def usuario(self):
        return self.__usuario


cuenta = CuentaWeb("sergio_1")
print(cuenta.usuario)

# CuentaWeb("1sergio")
