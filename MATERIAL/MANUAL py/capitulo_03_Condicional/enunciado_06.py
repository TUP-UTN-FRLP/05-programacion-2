# ============================================================
# Enunciado 6:
# Pedir tres números y determinar si el primero es mayor que el segundo y
# mayor que el tercero.
#
# NOTA: Como la condicion para evaluar si son digitos es muy larga PEP 8),
#       podemos hacer un salto de linea. PERO CUIDADO!, para que el compilador
#       no lo interprete como fin de sentencia, usamos parentesis, y
#       dentro de ellos hacemos el salto de linea.
#       Otra cosa importante, tenes que indentar la segunda linea, sino el
#       compilador no lo interpreta como parte de la condicion.
#
# NOTA: Si todos los valores ingresados los guardamos en una lista
#       respuestas = [respuesta_1, respuesta_2, respuesta_3]
#       y luego evaluarlo con un for que recorra la lista
#
#       if not all(numero.isdigit() for numero in numeros):
#
#       Probalo como anticipo al for
# ============================================================

# Titulo del programa
print()
print("Programa para evaluar si el primer numero es mayor")
print("==================================================")
print()

# ingreso de valores a comparar
respuesta_1 = input("Número 1: ")
respuesta_2 = input("Número 2: ")
respuesta_3 = input("Número 3: ")

# Evaluacion de los valores ingresados
# Si alguno de los valores ingresados no es un numero entero
# se muestra un mensaje de error
# Si todos los valores son numeros enteros, se comparan y se muestra
# un mensaje indicando si el primero es mayor o no
if (not respuesta_1.isdigit() or
        not respuesta_2.isdigit() or
        not respuesta_3.isdigit()):
    print("Todos los valores deben ser números enteros.")
else:
    numero_1 = int(respuesta_1)
    numero_2 = int(respuesta_2)
    numero_3 = int(respuesta_3)
    if all([numero_1 > numero_2, numero_1 > numero_3]):
        print("El primero es el mayor de todos")
    else:
        print("El primero no es el mayor")
