from validaciones_1 import validar_legajo


class Estudiante:
    def __init__(self, legajo):
        self.__legajo = validar_legajo(legajo)

    @property
    def legajo(self):
        return self.__legajo


estudiante = Estudiante(37101)
print(estudiante.legajo)

# Estudiante("37101")
