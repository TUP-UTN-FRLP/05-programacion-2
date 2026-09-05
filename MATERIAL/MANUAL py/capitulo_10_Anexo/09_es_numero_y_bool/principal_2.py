from validaciones_2 import validar_altura


class Persona:
    def __init__(self, altura):
        self.__altura = validar_altura(altura)

    @property
    def altura(self):
        return self.__altura


persona = Persona(1.75)
print(persona.altura)

# Persona(False)
