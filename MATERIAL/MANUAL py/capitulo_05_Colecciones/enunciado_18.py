# -*- coding: utf-8 -*-
# -----------------------------------------------------------
# Enunciado 18:
# Sistema de votos:
# Pedir votos al usuario para tres candidatos ("A", "B", "C")
# hasta que ingrese "fin".
# Al final, mostrar cuántos votos sacó cada uno
# y quién ganó.
# -----------------------------------------------------------

# Crear el diccionario con los tres candidatos
# comenzando todos con cero votos
votos = {
    "A": 0,
    "B": 0,
    "C": 0
}

# Pedir el primer voto y convertirlo a mayúscula
voto = input("Voto (A/B/C, o 'fin'): ").upper()

# Repetir mientras no se ingrese FIN
while voto != "FIN":

    # Verificar que el candidato exista
    if voto in votos:

        # Incrementar el contador correspondiente
        votos[voto] += 1

    else:
        print("Voto inválido")

    # Pedir el siguiente voto
    voto = input("Voto (A/B/C, o 'fin'): ").upper()

# Mostrar los resultados
print("\nResultado:")

for candidato, cantidad in votos.items():
    print(f"  {candidato}: {cantidad} votos")

# Buscar el candidato con mayor cantidad de votos
ganador = max(votos, key=votos.get)

# Mostrar el ganador
print(f"Ganó: {ganador}")
