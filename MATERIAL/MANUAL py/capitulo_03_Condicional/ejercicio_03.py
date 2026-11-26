# ============================================================
# Enunciado 3:
# Escribí un programa que pida un día de la semana (por ejemplo "lunes").
# Usá la función capitalize() para convertir la primera letra a mayúscula y
# luego la estructura match/case para imprimir:
# -"Inicio de semana" (Lunes)
# -"Mitad de semana" (Miércoles)
# -"Día normal" para el resto.
# Si ingresan cualquier otra cosa, imprimí "Dato no válido" usando el case _.
# ============================================================

# Pedir día de la semana al usuario
dia = input("Ingresa un día de la semana: ")

# Convertir primera letra a mayúscula
dia = dia.capitalize()

# Clasificar el día usando match/case
match dia:
    case "Lunes":
        print("Inicio de semana")
    case "Miércoles":
        print("Mitad de semana")
    case "Martes" | "Jueves" | "Viernes" | "Sábado" | "Domingo":
        print("Día normal")
    case _:
        print("Dato no válido")
