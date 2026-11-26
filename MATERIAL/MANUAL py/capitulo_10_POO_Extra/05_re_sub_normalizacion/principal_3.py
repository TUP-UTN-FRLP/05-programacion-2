from validaciones_3 import validar_descripcion


class Movimiento:
    def __init__(self, descripcion):
        self.__descripcion = validar_descripcion(descripcion)

    @property
    def descripcion(self):
        return self.__descripcion


movimiento = Movimiento("  Pago     de    servicio  ")
print(movimiento.descripcion)

# Caso invalido (supera 40 caracteres):
# Movimiento("A" * 41)

