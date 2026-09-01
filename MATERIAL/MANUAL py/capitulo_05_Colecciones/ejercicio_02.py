# -*- coding: utf-8 -*-
# ---------------------------------------------------
# Enunciado 2:
# Dos listas de amigos:
# mios = ["Ana", "Juan", "Pedro", "Lucía"]
# de_mi_hermano = ["Pedro", "Sofía", "Juan", "Diego"]
# Averiguá:
# - quiénes son amigos de los dos,
# - quiénes son solo míos,
# - quiénes son de alguno de los dos.
# ---------------------------------------------------

# Crear los sets de amigos
mios = {"Ana", "Juan", "Pedro", "Lucía"}
de_mi_hermano = {"Pedro", "Sofía", "Juan", "Diego"}

# Intersección: amigos que tenemos en común
comunes = mios & de_mi_hermano

# Diferencia: amigos que son solo míos
solo_mios = mios - de_mi_hermano

# Unión: todos los amigos, sin repetir
todos = mios | de_mi_hermano

# Mostrar los resultados
print(f"Amigos en común: {comunes}")
print(f"Solo míos: {solo_mios}")
print(f"En total (unidos, sin repetir): {todos}")
