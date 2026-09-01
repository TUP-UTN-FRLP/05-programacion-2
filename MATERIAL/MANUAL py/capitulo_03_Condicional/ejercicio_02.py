# ============================================================
# Enunciado 2:
# Escribí un programa que pida una edad y un género (ingresado como "M" o "F").
# Utilizá la función lower() del string ingresado para asegurarte de que
# funcione, aunque el usuario ingrese "m" o "f" minúscula.
# La persona debe ser mayor o igual a 18 años Y del género "F" para imprimir
# "Cumple para integrar equipos deportivos femeninos".
# En cualquier otro caso, imprimir "No cumple con el perfil".
#
# PREGUNTA: ¿Que ves si ingresas letras en edad?
#
# PREGUNTA: Dependemos del usuario para que el dato ingrese con el tipo }
#           correcto, ¿Como validamos?
#
# PREGUNTA: ¿Porque no convertimos el tipo del input de genero?
# ============================================================

# Pedir edad y genero al usuario
edad = int(input("Ingresa tu edad: "))
genero = input("Ingresa tu género (M/F): ")


# Convertir a minúscula con lower()
genero = genero.lower()


# Verificar si cumple con el perfil
if edad >= 18 and genero == "f":
    print("Cumple con el perfil buscado")
else:
    print("No cumple con el perfil")
