# ============================================================
# Enunciado 11:
# Verificar si un número ingresado es primo.
# Un número primo solo se divide por 1 y por sí mismo.
# ============================================================

# Pedir el número
numero = int(input("Número: "))

# Los números menores que 2 no son primos
if numero < 2:
    print("No es primo")
else:
    # Probar posibles divisores desde 2 hasta numero - 1
    for divisor in range(2, (numero) // 2 + 1):
        # Si encontramos un divisor exacto, no es primo
        if numero % divisor == 0:
            print("No es primo")
            break

    # El else del for se ejecuta si nunca usamos break
    else:
        print("Es primo")
