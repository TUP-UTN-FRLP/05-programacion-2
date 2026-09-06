from validaciones_3 import validar_clave


class Acceso:
    def __init__(self, clave):
        self.__clave = validar_clave(clave)

    def __repr__(self):
        return "Acceso(clave=<oculta>)"


acceso = Acceso("abc12345")
print(acceso)

# Acceso(12345678)
