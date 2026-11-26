# ============================================================
# Enunciado 17:
# Pedir un número de hasta 3 dígitos. Determinar si tiene 1, 2 o 3 dígitos.
# (Pista: si es menor a 10 tiene 1, si es menor a 100 tiene 2, si no, tiene 3).
#
# PREGUNTA: ¿Se peude usar un match?
# ============================================================

# Titulo del programa
print()
print("Programa de verificación de dígitos")
print("===================================")
print()

# Ingresar número
numero = input("Número: ")

# validación de dato ingresado
if not numero.isdecimal():
    print("Dato inválido")
    exit()

# lógica de verificación de dígitos
numero = int(numero)
if numero < 10:
    print("El número tiene 1 dígito")
elif numero < 100:
    print("El número tiene 2 dígitos")
elif numero < 1000:
    print("El número tiene 3 dígitos")
else:
    print("Mas de 3 dígitos")
