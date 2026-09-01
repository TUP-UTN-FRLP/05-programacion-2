# ============================================================
# Enunciado 4:
# Creá una tupla con las coordenadas de un punto en el plano
# y otra con los tres colores primarios RGB.
#
# Intentá modificar el primer valor de una de ellas
# y observá el error que da Python.
# ============================================================

# Crear una tupla con las coordenadas del punto
punto = (10, 25)

# Crear una tupla con los colores primarios
primarios = ("rojo", "verde", "azul")

# Mostrar las coordenadas del punto
print(f"El punto está en x={punto[0]}, y={punto[1]}")

# Mostrar el primer color
print(f"El primer color es {primarios[0]}")

# Esto genera un error porque las tuplas son inmutables
punto[0] = 50
