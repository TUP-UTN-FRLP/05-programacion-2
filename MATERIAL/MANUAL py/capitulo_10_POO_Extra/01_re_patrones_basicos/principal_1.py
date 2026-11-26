from validaciones_1 import validar_codigo


class Producto:
    def __init__(self, codigo):
        self.__codigo = validar_codigo(codigo)

    @property
    def codigo(self):
        return self.__codigo


producto = Producto("ABC123")
print(producto.codigo)

# Descomentar para observar el error:
# Producto("AB-123")
