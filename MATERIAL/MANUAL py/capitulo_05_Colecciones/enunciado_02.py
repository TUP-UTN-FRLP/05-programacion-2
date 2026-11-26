# -*- coding: utf-8 -*-
# ---------------------------------------------------------------
# Enunciado 2:
# Guardar la posición de un jugador en un mapa como tupla (x, y).
# Simular que el jugador se mueve una casilla a la derecha (x+1)
# creando una nueva tupla, y mostrar antes y después.
# ---------------------------------------------------------------


# Guardar la posición inicial del jugador como una tupla
posicion = (5, 3)

# Mostrar la posición inicial
print(f"Antes: {posicion}")

# Las tuplas no se pueden modificar.
# Creamos una nueva tupla y se la asignamos a posicion.
posicion = (posicion[0] + 1, posicion[1])

# Mostrar la nueva posición
print(f"Después: {posicion}")
