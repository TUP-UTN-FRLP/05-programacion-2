from validaciones_3 import validar_nombre


class Cliente:
    def __init__(self, nombre):
        self.__nombre = validar_nombre(nombre)

    @property
    def nombre(self):
        return self.__nombre


objeto = Cliente("o'connor")
print(objeto.nombre)

# Casos invalidos:
# Cliente("Ana123")     # tiene digitos
# Cliente("Ana_María")  # el guion bajo no es separador valido
