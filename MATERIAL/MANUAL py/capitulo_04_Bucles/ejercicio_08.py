# ============================================================
# Enunciado 8:
# Dada una lista de tareas pendientes, imprimir un checklist
# numerado empezando en 1.
# ============================================================

# Crear la lista de tareas
tareas = [
    "Revisar el TP",
    "Estudiar bucles",
    "Instalar Python",
    "Hacer ejercicios"
]

# enumerate() permite obtener el número y el contenido.
# start=1 hace que la numeración comience en 1.
for numero, tarea in enumerate(tareas, start=1):

    # Mostrar cada tarea como un elemento de checklist
    print(f"[ ] {numero}. {tarea}")
