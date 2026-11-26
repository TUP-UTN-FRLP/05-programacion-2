# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Ejercicio 4
# Escribí una función calcular_imc(peso, altura) que lance ValueError
# si el peso o la altura son menores o iguales a cero. Luego atrapá
# la excepción y mostrá el mensaje de error.
# -------------------------------------------------------------------------

def calcular_imc(peso, altura):
    if peso <= 0:
        raise ValueError("Peso debe ser positivo")
    if altura <= 0:
        raise ValueError("Altura debe ser positivo")
    return peso / (altura ** 2)


# calcular_imc() lanza ValueError si algún valor es <= 0.
# El except captura ese error y muestra el mensaje con "as e".
try:
    imc = calcular_imc(-70, -1.75)
    print(imc)
except ValueError as e:
    print(f"Error: {e}")
