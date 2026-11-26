# ============================================================
# Enunciado 5:
# Pedir un carácter y determinar si es una vocal (a, e, i, o, u).
# Considerar tanto mayúsculas como minúsculas.
#
# PREGUNTA: ¿Qué harías para que el programa no se rompa
#            si se ingresa más de un carácter?
# PREGUNTA: ¿Qué cambios harías para este programa sea mas flexible
#            evaluando otros tipos de caracteres? Si fueran digitos, como
#            simulás isdigit() o isalpha()?
# ============================================================
# Titulo del programa
print()
print("Programa para determinar vocales")
print("================================")
print()

# ingreso del caracter a evaluar
caracter = input("Ingrese un carácter: ")

# proceso: evaluamos si es vocal o no
# casefold() convierte a minúscula y mayúscula
# in es un operador que pregunta si el caracter está en la tupla de vocales
if caracter.casefold() in ('a', 'e', 'i', 'o', 'u'):
    print("Es vocal")
else:
    print("No es vocal")
