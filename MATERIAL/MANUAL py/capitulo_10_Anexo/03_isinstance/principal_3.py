from validaciones_3 import validar_activo


class Usuario:
    def __init__(self, activo):
        self.__activo = validar_activo(activo)

    @property
    def activo(self):
        return self.__activo


usuario = Usuario(True)
print(usuario.activo)

# Usuario(1)
