# ============================================================
# Enunciado 11:
# Pedir dos números y un operador (+, -, *, /).
# Usar match/case para realizar la operación matemática correspondiente e
# imprimir el resultado.
#
# PREGUNTA: ¿Que cambios harías si querés obtener resto y división entera?
# ============================================================

# Titulo del programa
print()
print("Programa de calculadora")
print("=======================")
print()

# Solicitud la edad y precio
numero_1 = input("Número 1: ")
numero_2 = input("Número 2: ")
operador = input("Operador (+, -, *, /): ")

# preparación de los números y operador ingresados
numero_1 = numero_1.replace(",", ".")
numero_2 = numero_2.replace(",", ".")
operador = operador.strip()

# Validación de los números ingresados
if (not numero_1.replace(".", "", 1).isdigit() or
        not numero_2.replace(".", "", 1).isdigit()):
    print("Error: Números inválidos")
elif operador not in ["+", "-", "*", "/"]:
    print("Error: Operador inválido")
else:
    # Conversión a números flotantes
    numero_1 = float(numero_1)
    numero_2 = float(numero_2)

    match operador:
        case "+":
            print(numero_1 + numero_2)
        case "-":
            print(numero_1 - numero_2)
        case "*":
            print(numero_1 * numero_2)
        case "/":
            if numero_2 != 0:
                print(numero_1 / numero_2)
            else:
                print("Error: no se puede dividir entre cero")
