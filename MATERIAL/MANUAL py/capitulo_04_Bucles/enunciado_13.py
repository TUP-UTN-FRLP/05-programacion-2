# ============================================================
# Enunciado 13:
# Pedir palabras por teclado hasta que el usuario ingrese
# "fin". Guardarlas en una lista y al final mostrarlas
# ordenadas alfabéticamente.
# ============================================================
# Crear una lista vacía
palabras = []
mensaje = "Ingrese palabras (escriba 'fin' para terminar):"

# Pedir la primera palabra
palabra = input(mensaje)

# Repetir mientras no se ingrese "fin"
while palabra.lower() != "fin":

    # Guardar la palabra
    palabras.append(palabra)

    # Pedir otra palabra
    palabra = input(mensaje)

# Ordenar las palabras
palabras_ordenadas = sorted(palabras)

# Mostrar las palabras ordenadas
print("Palabras ordenadas:")

for p in palabras_ordenadas:
    print(f" - {p}")
