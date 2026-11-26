# ============================================================
# Enunciado 20:
# Pedir una lista de notas y clasificar cuántas son:
# - Insuficientes (<4)
# - Aprobadas (4-6)
# - Buenas (7-8)
# - Excelentes (9-10)
#
# Mostrar un resumen:
# "Insuficientes: 2, Aprobadas: 5, ..."
# ============================================================

# Lista de notas
notas = [8, 3, 5, 9, 6, 10, 4, 7, 2, 8]

# Inicializar los contadores
insuficientes = 0
aprobadas = 0
buenas = 0
excelentes = 0

# Recorrer todas las notas
for nota in notas:

    # Notas menores a 4
    if nota < 4:
        insuficientes += 1

    # Como ya sabemos que no es menor a 4,
    # acá están las notas entre 4 y 6
    elif nota <= 6:
        aprobadas += 1

    # Como ya sabemos que no es menor o igual a 6,
    # acá están las notas entre 7 y 8
    elif nota <= 8:
        buenas += 1

    # El resto corresponde a notas 9 y 10
    else:
        excelentes += 1

# Mostrar el resumen
print(f"Insuficientes: {insuficientes}")
print(f"Aprobadas: {aprobadas}")
print(f"Buenas: {buenas}")
print(f"Excelentes: {excelentes}")
