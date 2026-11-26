from validaciones_2 import validar_stock


class Producto:
    def __init__(self, stock):
        self.__stock = validar_stock(stock)

    @property
    def stock(self):
        return self.__stock


producto = Producto(10)
print(producto.stock)

# Producto("10")
