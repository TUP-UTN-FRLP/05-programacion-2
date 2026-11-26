# ============================================================
# Enunciado 1:
# Pedir un número y mostrar si es par o impar (usando el operador módulo %).
#
# PREGUNTA 1: ¿El 0 es par?
# PREGUNTA 2: ¿Y si ingresamos un número negativo? Si da error, ¿Por qué?
# ============================================================

respuesta = input("Ingrese un número: ")

if respuesta.isdigit():
    numero = int(respuesta)
    if numero % 2 == 0:
        print(f"El número {numero} es Par")
    else:
        print(f"El número {numero} es Impar")
else:
    print("Error: No ingresaste un número válido.")
