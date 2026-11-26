# ==============================================================
# Enunciado 2:
# Pedir un número entero y calcular su factorial.
# Ejemplo: 5! = 5 · 4 · 3 · 2 · 1 = 120
#
# PREGUNTA: ¿Por que en el for, en el range ponemos nuemero + 1?
# ==============================================================

# Titulo
print()
print("************************")
print("* Calculo de FACTORIAL *")
print("************************")
print()

# Pedir el número al usuario, validarlo y convertirlo a entero
numero = input("Número: ")
if not numero.isdecimal():
    print("Ingreso no válido")
    exit()
numero = int(numero)

# lógica de cálculo
# El factorial comienza en 1 porque vamos a multiplicar
factorial = 1

# Recorrer desde 1 hasta el número ingresado
for i in range(1, numero + 1):
    factorial *= i

# Mostrar el resultado
print(f"El factorial de {numero} es {factorial}")
