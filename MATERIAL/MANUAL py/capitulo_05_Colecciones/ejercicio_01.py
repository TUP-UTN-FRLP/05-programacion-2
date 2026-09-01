# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# Enunciado 1:
# Una función podría querer devolver dos cosas, por ejemplo,
# dividir dos números y devolver cociente y resto.
# Como todavía no vimos funciones, simulá esto:
# guardá (cociente, resto) de dividir 47 por 5 en una tupla,
# y después desempaquetala en dos variables.
# Imprimí las dos por separado.
# ----------------------------------------------------------

# Guardar el cociente y el resto en una tupla
resultado = (47 // 5, 47 % 5)

# Desempaquetar la tupla en dos variables
cociente, resto = resultado

# Mostrar los resultados
print(f"Cociente: {cociente}")
print(f"Resto: {resto}")
