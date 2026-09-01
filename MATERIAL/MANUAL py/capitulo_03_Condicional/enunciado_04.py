# ============================================================
# Enunciado 4:
# Pedir la nota de un examen. Si es mayor o igual a 7, mostrar "Aprobado".
# Si es menor a 4, mostrar "Desaprobado". Si está entre 4 y 6 (inclusive),
# mostrar "A recuperatorio".
#
# PREGUNTA 1: ¿Qué pasa si el usuario ingresa un valor superior a 10?
# PREGUNTA 2: ¿Que pasa si ingresa un valor negativo?
# ============================================================

# Titulo del programa
print()
print("Programa para evaluar la nota de un examen")
print("==========================================")
print()

# ingreso nota del examen
respuesta = input("Ingrese la nota del alumno en digitos: ")

# Proceso: primero evaluar si es numerico, si no lo es, mostrar error.
# Si es numerico, convertir a int y evaluar
if not respuesta.isnumeric():
    print("Dato no numérico.")
else:
    nota = int(respuesta)
    if nota >= 7:
        print("Aprobado")
    elif nota >= 4:
        print("A recuperatorio")
    else:
        print("Desaprobado")
