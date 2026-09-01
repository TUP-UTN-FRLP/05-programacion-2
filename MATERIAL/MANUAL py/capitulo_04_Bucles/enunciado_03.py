# ============================================================
# Enunciado 3:
# Pedir 5 notas por teclado, guardarlas en una lista
# y mostrar el promedio.
# PREGUNTA: ¿Porqué en range() no ponemos +1?
#
# PREGUNTA: ¿Cómo mejorar la validación con un while?}
#
# PREGUNTA: ¿Cómo asegurar que las notas ingresadas esten
#           dentro del rango del 0 al 10
# ============================================================

# Titulo
print()
print("***********************")
print("* Calculo de PROMEDIO *")
print("***********************")
print()

# creamos una lista vacía para guardar los valores
notas = []

# Pedir las 5 notas validando al ingresar
for i in range(5):
    nota = input(f"Nota {i + 1}: ")
    if not nota.isdigit():
        print("Ingreso no válido")
        exit()
    else:
        nota = int(nota)
        notas.append(nota)

# Calcular el promedio
promedio = sum(notas) / len(notas)

# Mostrar el promedio con dos decimales
print(f"Promedio: {promedio:.2f}")
