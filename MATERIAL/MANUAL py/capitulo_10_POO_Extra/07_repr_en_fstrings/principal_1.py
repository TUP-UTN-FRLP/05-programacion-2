from validaciones_1 import validar_nombre_corto


class Contacto:
    def __init__(self, nombre):
        self.__nombre = validar_nombre_corto(nombre)

    @property
    def nombre(self):
        return self.__nombre


contacto = Contacto(" Ana ")
print(contacto.nombre)

# Contacto(" ")
