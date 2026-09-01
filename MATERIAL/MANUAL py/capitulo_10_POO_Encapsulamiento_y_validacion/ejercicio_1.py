# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Modificá la clase Persona del capítulo anterior (nombre, edad) para que
# la edad sea privada (_edad). Después probá acceder a persona._edad desde
# afuera y comprobá que funciona técnicamente, pero rompe el contrato.
#
# El archivo debe incluir la implementación y las pruebas mostradas en el
# ejercicio.
# -------------------------------------------------------------------------


class Persona:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self._edad = edad

    def presentarse(self):
        print(f"Soy {self.nombre} y tengo {self._edad} años")


persona = Persona("Ana", 30)
persona.presentarse()

# El guion bajo es solo una convención: Python NO impide el acceso.
# Técnicamente funciona:
print(persona._edad)          # 30

# Pero rompe el contrato: estamos tocando algo marcado como interno,
# y nada nos frena al asignar un valor inválido.
persona._edad = -5
persona.presentarse()         # Soy Ana y tengo -5 años

# Ese es el problema que resuelven las properties con validación
