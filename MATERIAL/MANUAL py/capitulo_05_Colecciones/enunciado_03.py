# -*- coding: utf-8 -*-
# ---------------------------------------------------------
# Enunciado 3:
# Usando desempaquetado de tuplas, intercambiar los valores
# de dos variables sin usar una variable auxiliar.
# ---------------------------------------------------------


# Crear las dos variables
a = 10
b = 20

# Mostrar los valores antes del intercambio
print(f"Antes: a={a}, b={b}")

# Intercambiar los valores mediante desempaquetado
a, b = b, a

# Mostrar los valores después del intercambio
print(f"Después: a={a}, b={b}")
