# ============================================================
# Enunciado 20:
# Pedir tres números enteros (positivos o cero).
# Determinar si todos son positivos o si hay al menos un cero.
# Imprimir el resultado.
#
# NOTA: Tenemos:
#     numero_1, numero_2, numero_3 = int(numero_1), int(numero_2),
#     int(numero_3)
#     una forma mas compacta es usando map()
#     numero_1, numero_2, numero_3 = map(int, (numero_1, numero_2, numero_3))
# ============================================================
# Titulo del programa
print()
print("Programa de verificación si un valor es 0")
print("=========================================")
print()

# Ingreso valores, validaciones y preparaciones
numero_1 = input("Número 1, debe ser 0 o positivo: ")
numero_2 = input("Número 2, debe ser 0 o positivo: ")
numero_3 = input("Número 3, debe ser 0 o positivo: ")

numeros = (numero_1, numero_2, numero_3)
if not all(numero.isdigit() for numero in numeros):
    print("Valores incorrectos")
    exit()
numero_1, numero_2, numero_3 = int(numero_1), int(numero_2), int(numero_3)

# logica de la verificación. Recordar que es isdigit() no valida negativos
if 0 in (numero_1, numero_2, numero_3):
    print("Hay al menos un cero")
else:
    print("Ninguno es cero")
