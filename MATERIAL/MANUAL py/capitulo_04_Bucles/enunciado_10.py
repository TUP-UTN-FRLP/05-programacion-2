# ============================================================
# Enunciado 10:
# Pedir 10 números y contar cuántos son positivos,
# cuántos negativos y cuántos son cero.
#
# NOTA: Analicemos este código que es un salto en hacer un
#       código más robusto. En este caso, se está pidiendo al
#       usuario que ingrese un número, luego se valida si el
#       valor ingresado es realmente un número. Le falta un
#       detalle, cada vez que falla la validacion perdemos una
#       iteracion. Se soluciona con un while.
#
#       Veamos:
#       if (not numero.isdigit() and
#           not (numero.startswith('-') and numero[1:].isdigit())):
#           print("Por favor, ingrese un número válido.")
#          continue
#       Primero preguntamos si no son todos digitos (caso positivo)
#       y luego preguntamos si no empieza con un signo negativo y
#       el resto son digitos (caso negativo). Si no se cumple ninguna
#       de las dos condiciones, entonces el valor ingresado no es
#       un número válido y se le pide al usuario que ingrese un
#       número nuevamente. Ahi viene continue() que vuelve a
#       empezar el ciclo for, sin ejecutar el resto del código.
# ============================================================

# Inicializar los tres contadores
positivos = 0
negativos = 0
ceros = 0

# Repetir 10 veces
for i in range(10):

    # Pedir un número
    numero = input(f"Número {i + 1}: ")
    if (not numero.isdigit() and
            not (numero.startswith('-') and numero[1:].isdigit())):
        print("Por favor, ingrese un número válido.")
        continue
    numero = int(numero)

    # Clasificar el número
    if numero > 0:
        positivos += 1
    elif numero < 0:
        negativos += 1
    else:
        ceros += 1

# Mostrar los resultados
print(f"Positivos: {positivos}")
print(f"Negativos: {negativos}")
print(f"Ceros: {ceros}")
