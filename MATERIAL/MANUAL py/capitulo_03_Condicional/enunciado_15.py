# ============================================================
# Enunciado 15:
# Pedir el estado civil de una persona
# (S para soltero, C para casado, D para divorciado).
# Usar match/case.
# -Si es "C", pedir la cantidad de hijos y mostrar "Tiene X hijos".
#
# PREGUNTA: ¿Porque en el caso de casado, se pide la cantidad de hijos
# y no se convierte a int?
# ============================================================

# Titulo del programa
print()
print("Programa de estado civil")
print("========================")
print()

# Ingresar estado civil
estado = input("Estado civil (S, C, D): ").strip()

# Validar que el estado civil sea una letra
if not estado.isalpha():
    print("Dato inválido")
    exit()

estado = estado.upper()
match estado:
    case "C":
        hijos = input("Cantidad de hijos: ")
        if not hijos.isdigit():
            print("Dato inválido")
            exit()
        print(f"Tiene {hijos} hijos")
    case "S":
        print("Soltero")
    case "D":
        print("Divorciado")
    case _:
        print("Dato inválido")
