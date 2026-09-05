from validaciones_3 import validar_temperatura


class Medicion:
    def __init__(self, temperatura):
        self.__temperatura = validar_temperatura(temperatura)

    @property
    def temperatura(self):
        return self.__temperatura


medicion = Medicion(23.5)
print(medicion.temperatura)

# Medicion(True)
