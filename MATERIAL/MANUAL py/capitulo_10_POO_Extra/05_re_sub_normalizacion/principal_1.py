from validaciones_1 import validar_nombre


class Persona:
    def __init__(self, nombre):
        self.__nombre = validar_nombre(nombre)

    @property
    def nombre(self):
        return self.__nombre


persona = Persona("   maría     josé   ")
print(persona.nombre)

# Caso invalido:
# Persona("Ana 123")

