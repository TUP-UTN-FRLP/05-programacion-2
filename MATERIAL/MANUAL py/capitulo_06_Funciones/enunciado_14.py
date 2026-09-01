# -*- coding: utf-8 -*-
# -------------------------------------------------------------------
# Enunciado 14:
# Escribí una función calculadora(a, b, op) que reciba dos números
# y un string con la operación ("+", "-", "*", "/").
# La función debe devolver el resultado.
# Si el operador es inválido, debe devolver None.
# -------------------------------------------------------------------


def calculadora(a, b, op):
    if op == "+":
        return a + b

    if op == "-":
        return a - b

    if op == "*":
        return a * b

    if op == "/":
        if b == 0:
            return None

        return a / b

    return None


print(calculadora(10, 5, "+"))
print(calculadora(10, 5, "/"))
print(calculadora(10, 0, "/"))
print(calculadora(10, 5, "?"))
