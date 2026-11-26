# ============================================================
# Enunciado 19:
# Dada una calificación numérica del 1 al 10, usar match/case con la sintaxis
# de unión de casos (case 1 | 2 | 3:) para agrupar y mostrar:
# -"Insuficiente" (1-3)
# -"Regular" (4-5)
# -"Bien" (6-7)
# -"Muy Bien" (8-9)
# -"Sobresaliente" (10).
# ============================================================
# Titulo del programa
print()
print("Programa de calificación examen")
print("===============================")
print()

# Ingresar nota
nota = input("Nota (1-10): ")

# Validación ingreso
if not nota.isdecimal():
    print("Dato incorrecto")
    exit()
nota = int(nota)

# logica de la clasificacion
match nota:
    case 1 | 2 | 3:
        print("Insuficiente")
    case 4 | 5:
        print("Regular")
    case 6 | 7:
        print("Bien")
    case 8 | 9:
        print("Muy Bien")
    case 10:
        print("Sobresaliente")
    case _:
        print("Nota fuera de rango")
