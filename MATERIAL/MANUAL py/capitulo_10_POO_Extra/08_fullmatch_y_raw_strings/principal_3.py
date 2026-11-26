from validaciones_3 import validar_telefono


class Contacto:
    def __init__(self, telefono):
        self.__telefono = validar_telefono(telefono)

    @property
    def telefono(self):
        return self.__telefono


contacto = Contacto("+542211234567")
print(contacto.telefono)

# Contacto("2211234567")
