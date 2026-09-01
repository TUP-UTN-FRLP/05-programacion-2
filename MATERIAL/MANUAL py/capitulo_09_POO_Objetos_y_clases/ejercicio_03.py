# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Ejercicio 3
# Creá una clase Alumno con atributos nombre, edad y promedio. Agregale
# un método presentarse() que imprima algo como "Soy Ana, tengo 22 años
# y mi promedio es 8.5". Después creá dos alumnos distintos y hacé que
# cada uno se presente.
# -------------------------------------------------------------------------


class Alumno:

    def __init__(self, nombre, edad, promedio):
        self.nombre = nombre
        self.edad = edad
        self.promedio = promedio

    def presentarse(self):
        print(
            f"Soy {self.nombre}, tengo {self.edad} años "
            f"y mi promedio es {self.promedio}"
        )


ana = Alumno("Ana", 22, 8.5)
juan = Alumno("Juan", 25, 7.2)

ana.presentarse()
juan.presentarse()
