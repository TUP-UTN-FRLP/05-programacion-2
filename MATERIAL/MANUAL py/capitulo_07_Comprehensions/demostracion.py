cuadrados = []

for numero in range(1, 11):
    cuadrados.append(numero ** 2)

print(cuadrados)

# [expresión for elemento in colección]

cuadrados_comp = [numero ** 2 / 2 for numero in range(1, 11)]
print(cuadrados_comp)
