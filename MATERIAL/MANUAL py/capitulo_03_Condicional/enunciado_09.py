# ============================================================
# Enunciado 9:
# Un teatro ofrece descuentos:
# -menores de 18 pagan 50%
# -mayores de 65 pagan 30%
# Pedir edad y el precio base de la entrada, mostrar el precio final.
#
# NOTA: Observa el uso de dos funciones. Se evaluan de izquierda a derecha
#       si la primera es falsa, no se evalúa la segunda.
#
# PREGUNTA: ¿Porque en replace(".", "", 1) usamos 1 como tercer parámetro?
#
# PREGUNTA: ¿Porque este no cambia el valor de preci0 "sacando" el punto
#           decimal?
# PREGUNTA: ¿Por que print(f"Precio final: ${precio_final:.2f}") esta identado?
#           ¿Cómo puedo evitar que, si lo pusiera sin identación, no se
#           dispare el mensaje?
# ============================================================

# Titulo del programa
print()
print("Programa de descuentos de teatro")
print("================================")
print()

# Solicitud la edad y precio
edad = input("Ingrese edad: ")
precio = input("Ingrese precio entrada: ")

# tomamos en cuanta que el usuario puede ingresar el precio
# con coma o punto decimal. Reemplazamos la coma por punto
# para poder convertirlo a float
precio = precio.replace(",", ".")

# evaluamos si ingresa número válido, si no es así,
# mostramos un mensaje de error
if not edad.isdecimal() or not precio.replace(".", "", 1).isdigit():
    print("Datos inválidos")
else:
    edad = int(edad)
    precio = float(precio)
    print(precio)
    if edad < 18:
        precio_final = precio * 0.50
    elif edad >= 65:
        precio_final = precio * 0.30
    else:
        precio_final = precio

    print(f"Precio final: ${precio_final:.2f}")
