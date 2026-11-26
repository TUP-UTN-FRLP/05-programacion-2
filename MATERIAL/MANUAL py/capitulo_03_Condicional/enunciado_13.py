# ============================================================
# Enunciado 13:
# Determinar si un triángulo es isósceles, equilátero o escaleno
# pidiendo los tres lados por teclado.
# (Verificar antes si los lados forman un triángulo válido)
#
# NOTA: Observar en la conversión de tipos, la asignación múltiple
# ============================================================

# Titulo del programa
print()
print("Programa para clasificar triángulos")
print("===================================")
print()

# Solicitud de los tres lados
lado_1 = input("Lado 1: ")
lado_2 = input("Lado 2: ")
lado_3 = input("Lado 3: ")

if (not lado_1.isdigit() or
        not lado_2.isdigit() or
        not lado_3.isdigit()):
    print("Datos inválidos")
else:
    lado_1, lado_2, lado_3 = int(lado_1), int(lado_2), int(lado_3)

    # Para verificar si es un triángulo válido,
    # se debe cumplir la condición de que la suma de dos lados
    # debe ser mayor que el tercer lado
    if not (lado_1 + lado_2 > lado_3 and
            lado_1 + lado_3 > lado_2 and
            lado_2 + lado_3 > lado_1):
        print("No forman un triángulo")
    elif lado_1 == lado_2 == lado_3:
        print("Equilátero")
    elif lado_1 == lado_2 or lado_1 == lado_3 or lado_2 == lado_3:
        print("Isósceles")
    else:
        print("Escaleno")
