from validaciones_2 import validar_ciudad


class Sucursal:
    def __init__(self, ciudad):
        self.__ciudad = validar_ciudad(ciudad)

    @property
    def ciudad(self):
        return self.__ciudad


sucursal = Sucursal("La Plata")
print(sucursal.ciudad)

# Caso invalido:
# Sucursal("La Plata 2")

