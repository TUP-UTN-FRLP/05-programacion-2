# ============================================================
# Enunciado 2:
# Pedir dos números y mostrar cuál de los dos es mayor. Si son iguales,
# mostrar "Son iguales".
#
# PREGUNTA: ¿Cómo mejorar el código si quiero comparar tres números?
# ============================================================

respuesta_1 = input("Número 1: ")
respuesta_2 = input("Número 2: ")

if not respuesta_1.isdigit() or not respuesta_2.isdigit():
    print("Error: No ingresaste números válidos.")
else:
    numero_1 = int(respuesta_1)
    numero_2 = int(respuesta_2)
    if numero_1 == numero_2:
        print("Son iguales")
    else:
        print(f"El mayor es {max(numero_1, numero_2)}")
