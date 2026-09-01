# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 16
# Un juego de adivinar el número: el programa piensa un número entre
# 1 y 100 (usá random.randint(1, 100)), el usuario intenta hasta
# acertar. Manejar entradas no numéricas sin cortar el juego.
# -------------------------------------------------------------------------


import random


secreto = random.randint(1, 100)
intentos = 0


while True:
    # int() falla con ValueError si el usuario ingresa texto.
    # El except muestra el aviso y continue reinicia el bucle.
    try:
        intento = int(input("Adiviná (1-100): "))

    except ValueError:
        print("Ingresá un número")
        continue

    intentos += 1

    if intento < secreto:
        print("Más alto")
    elif intento > secreto:
        print("Más bajo")
    else:
        print(f"¡Acertaste en {intentos} intentos!")
        break
