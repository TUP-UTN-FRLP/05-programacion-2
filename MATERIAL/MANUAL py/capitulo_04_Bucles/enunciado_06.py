# ============================================================
# Enunciado 6:
# Imprimir la tabla de multiplicar del número que ingrese
# el usuario, del 1 al 10.
# ============================================================

# Titulo
print()
print("************************")
print("* Tabla de Multiplicar *")
print("************************")
print()

# Pedir el número al usuario
numero = int(input("Tabla de: "))


# Recorrer los números del 1 al 10
for i in range(1, 11):

    # Mostrar cada multiplicación
    print(f"{numero} x {i} = {numero * i}")
