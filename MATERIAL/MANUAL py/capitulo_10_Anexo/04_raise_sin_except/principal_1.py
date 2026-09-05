from validaciones_1 import validar_edad


class Persona:
    def __init__(self, edad):
        self.__edad = validar_edad(edad)

    @property
    def edad(self):
        return self.__edad


persona = Persona(25)
print(persona.edad)

# No hay try/except. Si se descomenta, la excepcion se propaga
# y Python detiene la ejecucion mostrando el traceback.
# Persona(-1)
