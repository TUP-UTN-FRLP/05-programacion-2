# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Ejercicio 1
# Definí una clase vacía llamada Persona. Creá tres objetos de esa clase
# (persona1, persona2, persona3) e imprimí cada uno. Comprobá con
# isinstance() que efectivamente son de tipo Persona.
# -------------------------------------------------------------------------


class Persona:
    pass


persona1 = Persona()
persona2 = Persona()
persona3 = Persona()

# Imprime los objetos según la representación por defecto de Python,
# que incluye el tipo de objeto y su dirección en memoria.
print(persona1)
print(persona2)
print(persona3)

print(isinstance(persona1, Persona))
print(isinstance("hola", Persona))
