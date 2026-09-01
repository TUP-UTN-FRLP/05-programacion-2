# ============================================================
# Enunciado 14:
# Un vendedor recibe una comisión:
# -si vende más de 5000, tiene 10% de comisión sobre el excedente.
# -Si vende entre 2000 y 5000, tiene 5% sobre el excedente.
# -Si vende menos de 2000, no tiene comisión.
# Pedir las ventas totales y calcular la comisión.
#
# NOTA: Acá utilizamos la función exit(). De esta manera el programa termina
#       en ese punto, no hay peligro que se ejecute otra cosa y podemos
#       separa el if de validación de la lógica de cálculo de comisiones.
# ============================================================

# Titulo del programa
print()
print("Programa de calculadora de comisiones")
print("=====================================")
print()

# Ingresar valor de ventas
ventas = input("Ventas totales: ")
comision = 0

# preparación de la variable ventas para el cálculo
ventas = ventas.replace(",", ".")

# Validar que el valor ingresado sea un número
if not ventas.replace(".", "", 1).isdigit():
    print("Error: Debe ingresar un número válido.")
    exit()

# lógica de cálculo de comisiones
ventas = float(ventas)
if ventas > 5000:
    comision = (ventas - 5000) * 0.10
elif ventas >= 2000:
    comision = (ventas - 2000) * 0.05

print(f"Comisión: ${comision:.2f}")
