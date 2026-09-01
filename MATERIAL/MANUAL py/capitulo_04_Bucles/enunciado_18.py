# ============================================================
# Enunciado 18:
# Dada una frase, contar cuántas palabras tiene
# y cuál es la más larga.
# ============================================================

# Pedir una frase
frase = input("Frase: ")

# Separar la frase en palabras
palabras = frase.split()

# Mostrar la cantidad de palabras
print(f"Cantidad de palabras: {len(palabras)}")

# Comenzar con una palabra más larga vacía
mas_larga = ""

# Recorrer todas las palabras
for palabra in palabras:

    # Comparar la longitud de cada palabra
    if len(palabra) > len(mas_larga):
        mas_larga = palabra

# Mostrar la palabra más larga
print(f"La más larga: '{mas_larga}' ({len(mas_larga)} letras)")
