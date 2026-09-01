# ============================================================
# Enunciado 8:
# Contar cuántas vocales tiene una palabra ingresada
# por el usuario.
# ============================================================

# Pedir la palabra y convertirla a minúsculas
palabra = input("Palabra: ").casefold()

# Inicializar el contador de vocales
contador = 0

# Recorrer cada letra de la palabra
for letra in palabra:

    # Verificar si la letra es una vocal
    if letra in ('a', 'e', 'i', 'o', 'u'):
        contador += 1

# Mostrar la cantidad de vocales
print(f"Tiene {contador} vocales")
