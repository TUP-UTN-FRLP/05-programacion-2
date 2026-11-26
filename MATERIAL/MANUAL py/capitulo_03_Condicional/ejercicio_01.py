# ============================================================
# Enunciado 1:
# Escribí un programa que pida al usuario un número.
# Antes de verificar si es positivo o cero, usá un if para comprobar
# que el usuario no haya ingresado letras (podés usar la función de
# strings isdigit()).
# Si ingresó letras, mostrá un error.
# Si no, evaluá el número e imprimí "Positivo", "Cero" o "Negativo".
#
# PREGUNTA: El siguiente código no valida si es negativo, ¿Porqué?
#           Mejoralo
# ============================================================

# Pedir número al usuario
entrada = input("Ingresa un número: ")

# Verificar si contiene solo dígitos
if not entrada.isdigit():
    print("Error: Ingresaste letras. Debes ingresar un número.")
else:
    # Convertir a entero
    numero = int(entrada)

    # Evaluar si es positivo, negativo o cero
    if numero > 0:
        print("Positivo")
    elif numero < 0:
        print("Negativo")
    else:
        print("Cero")
