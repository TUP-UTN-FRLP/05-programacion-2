from validaciones_3 import validar_patente


class Vehiculo:
    def __init__(self, patente):
        self.__patente = validar_patente(patente)

    @property
    def patente(self):
        return self.__patente


vehiculo = Vehiculo("ab123cd")
print(vehiculo.patente)

# Vehiculo("ABC123")
