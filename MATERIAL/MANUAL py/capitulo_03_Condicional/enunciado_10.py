# ============================================================
# Enunciado 10:
# Pedir el nombre de un día de la semana (por ejemplo, "lunes" o "MARTES").
# Usar match/case para clasificarlo en "Inicio de semana", "Mitad de semana",
# "Casi fin de semana" o "Fin de semana", sin importar cómo lo haya escrito el
# usuario. Si no es un día válido, mostrar "Dato no válido".
#
# Solución:
# dia = input("Día de la semana: ").capitalize()
#
# match dia:
#     case "Lunes":
#         print("Inicio de semana")
#     case "Martes" | "Miércoles" | "Jueves":
#         print("Mitad de semana")
#     case "Viernes":
#         print("Casi fin de semana")
#     case "Sábado" | "Domingo":
#         print("Fin de semana")
#     case _:
#         print("Dato no válido")
# ============================================================

# Titulo del programa
print()
print("Programa de clasificación de días de la semana")
print("==============================================")
print()

# Solicitar día de la semana

dia = input("Día de la semana: ").capitalize()

match dia:
    case "Lunes":
        print("Inicio de semana")
    case "Martes" | "Miércoles" | "Jueves":
        print("Mitad de semana")
    case "Viernes":
        print("Casi fin de semana")
    case "Sábado" | "Domingo":
        print("Fin de semana")
    case _:
        print("Dato no válido")
