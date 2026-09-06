from validaciones_2 import validar_codigo


class Articulo:
    def __init__(self, codigo):
        self.__codigo = validar_codigo(codigo)

    @property
    def codigo(self):
        return self.__codigo


articulo = Articulo("A-100")
print(articulo.codigo)

# Articulo("A 100")
