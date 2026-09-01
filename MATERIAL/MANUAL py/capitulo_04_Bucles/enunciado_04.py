# ============================================================
# Enunciado 4:
# Pedir números al usuario hasta que ingrese 0.
# Al terminar, mostrar cuántos números ingresó y su promedio,
# sin contar el 0.
# ============================================================

# Crear una lista vacía para guardar los números
numeros = []
mensaje = "Ingrese números (0 para terminar): "
# Pedir el primer número antes del while
numero = input(mensaje)

# Validamos entrada, no esta especificado si es entero o flotante
# así que validamos con isdecimal() garantizando que sean solo digitos
# y no otros caracteres como superindice o subindices
# y luego lo convertimos a float
if not numero.replace('.', '', 1).isdigit():
    print("Ingreso no válido")
    exit()
numero = float(numero)

# Repetir mientras el número sea diferente de 0
while numero != 0:
    numeros.append(numero)

    # Pedir otro número
    numero = input(mensaje)
    if not numero.replace('.', '', 1).isdigit():
        print("Ingreso no válido")
        exit()
    numero = float(numero)

# Verificar que se haya ingresado al menos un número
if len(numeros) > 0:
    print(f"Ingresaste {len(numeros)} números")
    print(f"Promedio: {sum(numeros) / len(numeros):.2f}")
else:
    print("No ingresaste números")
