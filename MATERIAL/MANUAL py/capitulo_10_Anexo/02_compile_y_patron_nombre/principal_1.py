from validaciones_1 import validar_nombre


class Persona:
    def __init__(self, nombre):
        self.__nombre = validar_nombre(nombre)

    @property
    def nombre(self):
        return self.__nombre


objeto = Persona("maría")
print(objeto.nombre)

# Casos invalidos:
# Persona("Ana123")        # tiene digitos
# Persona("maria jose")    # este paso todavia no acepta espacios
