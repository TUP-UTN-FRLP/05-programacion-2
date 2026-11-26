# -*- coding: utf-8 -*-
# ------------------------------------------------------------
# Enunciado 3:
# Simulá un sistema de "materias aprobadas".
# Empezá con un set vacío, agregá tres materias que aprobaste,
# y chequeá si aprobaste "Programación 2".
# ------------------------------------------------------------

# Crear un set vacío
aprobadas = set()

# Agregar materias aprobadas
aprobadas.add("Álgebra")
aprobadas.add("Análisis Matemático")
aprobadas.add("Programación 1")

# Comprobar si Programación 2 está entre las materias aprobadas
if "Programación 2" in aprobadas:
    print("Ya la aprobaste")
else:
    print("Todavía no aprobaste Programación 2")
