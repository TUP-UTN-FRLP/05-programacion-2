# -*- coding: utf-8 -*-
# ---------------------------------------------
# Enunciado 8:
# Sumar los cuadrados de los pares del 1 al 10.
# Resolverlo utilizando una forma pythónica.
# ---------------------------------------------

# Recorrer los números del 0 al 10,
# seleccionar solamente los pares,
# elevarlos al cuadrado y sumarlos.
suma = sum(x**2 for x in range(11) if x % 2 == 0)

# Mostrar el resultado
print(suma)
