# -*- coding: utf-8 -*-
# ---------------------------------------
# Enunciado 14:
# Mini agenda:
# Usar un diccionario {nombre: teléfono}.
# Ofrecer un menú con las opciones:
# 1. Agregar contacto
# 2. Buscar
# 3. Eliminar
# 4. Listar todos
# 5. Salir
# Repetir hasta que elija salir.
# ---------------------------------------

# crear la agenda vacía
agenda = {}

# inicializar la variable de opción
opcion = ""

# lógica del menú: repetir hasta que elija salir
while opcion != "5":

    print()
    print("--- AGENDA ---")
    print("1. Agregar contacto")
    print("2. Buscar")
    print("3. Eliminar")
    print("4. Listar todos")
    print("5. Salir")
    print("--------------")

    opcion = input("Elegí una opción (1-5): ")

    match opcion:

        case "1":
            nombre = input("Nombre: ")
            telefono = input("Teléfono: ")

            agenda[nombre] = telefono
            print("Contacto agregado")

        case "2":
            nombre = input("Nombre a buscar: ")
            print(f"{nombre}: {agenda.get(nombre, 'No está en la agenda')}")

        case "3":
            nombre = input("Nombre a eliminar: ")

            if nombre in agenda:
                del agenda[nombre]
                print("Eliminado")
            else:
                print("No estaba en la agenda")

        case "4":
            if len(agenda) == 0:
                print("Agenda vacía")
            else:
                for nombre, tel in agenda.items():
                    print(f"  {nombre}: {tel}")

        case "5":
            print("Chau")

        case _:
            print("Opción inválida")
