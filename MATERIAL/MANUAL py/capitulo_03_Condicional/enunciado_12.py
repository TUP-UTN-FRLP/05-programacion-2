# ============================================================
# Enunciado 12:
# Pedir un año e indicar si es bisiesto o no. Un año es bisiesto si:
# -es divisible por 4
# -pero no por 100, a menos que también sea divisible por 400.
# ============================================================

# Titulo del programa
print()
print("Programa para detectar años bisiestos")
print("=====================================")
print()

# Solicitud la edad y precio

anio = input("Año: ")

if not anio.isdecimal():
    print("Año inválido")
else:
    anio = int(anio)
    if (anio % 4 == 0 and anio % 100 != 0) or (anio % 400 == 0):
        print("Es bisiesto")
    else:
        print("No es bisiesto")
