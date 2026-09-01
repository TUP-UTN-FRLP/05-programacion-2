# ============================================================
# Enunciado 18:
# Un casino permite el ingreso a mayores de 21 años. También permite
# el ingreso a menores de 21 si están acompañados de un tutor legal
# (ingresado como la palabra "True" o "False").
# Pedir edad y si está acompañado.
# Mostrar "Puede ingresar" o "No puede ingresar".
#
# NOTA: Una de las comfusiones mas comunes está en esta línea:
#       if acompaniado not in ("True", "False"):
#       podiamos haber puesto:
#       if not acompaniado == "True" or not acompaniado == "False"
#       Esto no es correcto ya que se podría caer en la confusión
#       de usar un or o un and. Lo mejor es usar el in que es mas
#       flexible
#
#       PREGUNTA: ¿Lo que hacemos acá es redundancia o es necesario?
#                 elif acompaniado == "True":
#                     acompaniado = True
#                 else:
#                     acompaniado = False
#                 ¿Por qué?
# ============================================================
# Titulo del programa
print()
print("Programa de verificación de ingreso al casino")
print("=============================================")
print()

# Ingresar edad, validacion de la entrada y preparacion
edad = input("Edad: ")
if not edad.isdecimal():
    print("valor incorrecto")
    exit()
edad = int(edad)

# Si es menor 21 ingresar acompañante y validacion de la entrada
if edad < 21:
    acompaniado = input("¿Tiene acompañante (True/False)?: ")
    acompaniado = acompaniado.replace(" ", "").capitalize()
    if acompaniado not in ("True", "False"):
        print("Dato inválido")
        exit()
    elif acompaniado == "True":
        acompaniado = True
    else:
        acompaniado = False

# logica de ingreso
if edad >= 21 or (edad < 21 and acompaniado):
    print("Puede ingresar")
else:
    print("No puede ingresar")
