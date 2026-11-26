from validaciones_1 import validar_dni


class Persona:
    def __init__(self, dni):
        self.__dni = validar_dni(dni)

    @property
    def dni(self):
        return self.__dni


persona = Persona("12345678")
print(persona.dni)

# Persona("12.345.678")
