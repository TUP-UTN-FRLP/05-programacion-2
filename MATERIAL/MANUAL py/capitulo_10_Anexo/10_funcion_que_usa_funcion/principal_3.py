from validaciones_3 import validar_apellido, validar_nombre


class Persona:
    def __init__(self, nombre, apellido):
        self.__nombre = validar_nombre(nombre)
        self.__apellido = validar_apellido(apellido)

    @property
    def nombre_completo(self):
        return f"{self.__apellido}, {self.__nombre}"


persona = Persona("ana maría", "pérez")
print(persona.nombre_completo)

# Persona("Ana123", "Perez")
