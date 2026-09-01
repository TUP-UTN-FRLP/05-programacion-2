# ============================================================
# Enunciado 7:
# Imprimir todos los números pares del 2 al 20 usando
# range() con paso.
#
# Después, hacer la cuenta regresiva de 10 a 1
# en la misma línea.
# ============================================================

# Pares del 2 al 20
# El tercer parámetro de range() indica el paso
for n in range(2, 21, 2):
    print(n)

# Cuenta regresiva de 10 a 1
# El paso -1 hace que vayamos hacia atrás
for n in range(10, 0, -1):
    print(n, end=" ")

# Mostrar el mensaje al finalizar la cuenta
print("¡Despegue!")
