from validaciones_3 import validar_observacion


class Registro:
    def __init__(self, observacion):
        self.__observacion = validar_observacion(observacion)

    @property
    def observacion(self):
        return self.__observacion


registro = Registro("Sin novedades")
print(registro.observacion)

# Registro("  Sin novedades  ")
