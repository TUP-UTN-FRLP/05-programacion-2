from validaciones_2 import validar_promedio


class Alumno:
    def __init__(self, promedio):
        self.__promedio = validar_promedio(promedio)

    @property
    def promedio(self):
        return self.__promedio


alumno = Alumno(8.5)
print(alumno.promedio)

# Alumno(True)
