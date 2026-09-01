# ============================================================
# Enunciado 15:
# Adivinanza: el programa "piensa" el número 42.
# Pedir intentos al usuario hasta que acierte,
# indicándole si su intento es mayor o menor.
# ============================================================

# Definir el número secreto
numero_secreto = 42

# Pedir el primer intento
intento = int(input("Adiviná el número: "))

# Repetir mientras el intento sea incorrecto
while intento != numero_secreto:

    # Indicar si el número ingresado es menor
    if intento < numero_secreto:
        print("Es mayor")
    else:
        print("Es menor")

    # Pedir un nuevo intento
    intento = int(input("Adiviná el número: "))

# Llegamos acá cuando el usuario acertó
print("¡Correcto!")
