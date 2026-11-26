# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 19
# Pedile al usuario 5 números y guardá los válidos en una lista.
# Los que fallen (letras, strings vacíos, etc.) los ignorás sin
# cortar el programa. Al final, mostrar la lista y cuántos ingresó
# válidamente.
# -------------------------------------------------------------------------


validos = []

for i in range(5):
    entrada = input(f"Número {i + 1}: ")

    # float() falla con ValueError si la entrada es texto o está vacía.
    # El except muestra el aviso y el bucle sigue con el siguiente número.
    try:
        validos.append(float(entrada))
    except ValueError:
        print(f"  '{entrada}' no es un número, se ignora")

print(f"\nIngresaste {len(validos)} números válidos: {validos}")
