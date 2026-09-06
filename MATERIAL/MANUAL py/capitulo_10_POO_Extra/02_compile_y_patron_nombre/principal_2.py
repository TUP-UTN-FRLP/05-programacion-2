from validaciones_2 import validar_nombre


class Autor:
    def __init__(self, nombre):
        self.__nombre = validar_nombre(nombre)

    @property
    def nombre(self):
        return self.__nombre


objeto = Autor("juan pablo")
print(objeto.nombre)

# Casos invalidos:
# Autor("Ana123")        # tiene digitos
# Autor("juan-pablo")    # este paso todavia no acepta guiones
