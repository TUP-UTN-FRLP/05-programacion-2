# ============================================================
# Enunciado 16:
# Verificar si un número ingresado está entre 10 y 20, O si está entre 30 y 40.
# Si cumple alguna de las dos condiciones, mostrar
# "El número está en los rangos permitidos".
# ============================================================

# Titulo del programa
print()
print("Programa de verificación de rangos permitidos")
print("=============================================")
print()

# Ingresar número
numero = input("Ingrese número: ")

# Validación del tipo de dato ingresado
if not numero.isdigit():
    print("Dato inválido")
    exit()
numero = int(numero)

# lógica de verificación de rangos
if 10 <= numero <= 20 or 30 <= numero <= 40:
    print("El número está en los rangos permitidos")
else:
    print("Fuera de rango")
