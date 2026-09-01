# ============================================================
# Enunciado 7:
# Simular un login: Pedir usuario y contraseña. Validar que el usuario y la
# contraseña no sean solo espacios en blanco. Limpiar los espacios al inicio
# y final de ambas entradas. Si el usuario es "admin" y la contraseña es
# "1234", mostrar "Acceso concedido". Si no, mostrar "Acceso denegado".
#
# NOTA: Ojo con strip() saca espacios al inicio y al final, si se ingresa
#       uno o dos, al sacarlos DEJA UN STRING VACIO. No tiene espacios,
#       es vacío.
#       Ojo con isspace() que devuelve True si el string tiene solo espacios,
#       y False si tiene al menos un caracter que no sea espacio.
#       Si el resultado de strip() deja un str vacío, issspace() cree que
#       hay algo ya que pregunta si hay caracter espacio, no vacio
#
# PREGUNTA: ¿Cómo evitar que en dos lineas diferentes se imprima el
#           "acceso denegado" asi al cambiar el mensaje no me tenga que acordar
#           de cambiar en dos lugares?.
#           TIP: preguntate que pasa si aplico strip() cuando no ingreso ningún
#           caracter o cualquier número de espacios
#
# PREGUNTA: ¿Si quiero que tire error cuando no se ingresa
#           extricto admin y 1234
# ============================================================

# Titulo del programa
print()
print("Programa de login")
print("=================")
print()

# Solicitud de usuario y contraseña
usuario = input("Usuario: ")
contrasenia = input("Contraseña: ")

# proceso: evaluamos si el usuario y la contraseña son solo espacios en blanco
# luego limpiamos los espacios al inicio y final de ambas entradas
# finalmente evaluamos si el usuario y la contraseña son correctos
if usuario.isspace() or contrasenia.isspace():
    print("Acceso denegado")
else:            # Si cae acá es que por lo menos hay un caracter
    usuario = usuario.strip()
    contrasenia = contrasenia.strip()

    if usuario == "admin" and contrasenia == "1234":
        print("Acceso concedido")
    else:
        print("Acceso denegado")
