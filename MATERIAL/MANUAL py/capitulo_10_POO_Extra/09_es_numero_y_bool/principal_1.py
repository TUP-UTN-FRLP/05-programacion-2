from validaciones_1 import validar_precio


class Producto:
    def __init__(self, precio):
        self.__precio = validar_precio(precio)

    @property
    def precio(self):
        return self.__precio


producto = Producto(1500.50)
print(producto.precio)

# Producto(True)
