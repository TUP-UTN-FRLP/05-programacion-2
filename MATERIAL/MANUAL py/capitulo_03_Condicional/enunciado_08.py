# ============================================================
# Enunciado 8:
# Pedir la edad de una persona.
# Si es menor de 12, mostrar "Niño".
# Si es entre 12 y 17, mostrar "Adolescente".
# Si es entre 18 y 64, mostrar "Adulto".
# Si es 65 o más, mostrar "Adulto mayor".
#
# PREGUNTA: ¿Que diferencia hay entre usar isdigital(), isnumeric() y
#           isdecimal()
#           para validar la edad ingresada?
# PREGUNTA: ¿Porque no definimos valor por defecto?
# PREGUNTA: ¿Cómo validas que se ingrese edad coherente
#           como ser menor a 120 años?
# ============================================================

# Titulo del programa
print()
print("Programa de clasificación por edad")
print("==================================")
print()

# Solicitud la edad
respuesta = input("Edad: ")

# evaluamos si ingresa un número entero positivo,
# si no es así, mostramos un mensaje de error
if not respuesta.isdecimal():
    print("Edad inválida")
else:
    edad = int(respuesta)

    match edad:
        case edad if edad < 12:
            print("Niño")
        case edad if 12 <= edad <= 17:
            print("Adolescente")
        case edad if 18 <= edad <= 64:
            print("Adulto")
        case edad if edad >= 65:
            print("Adulto mayor")
