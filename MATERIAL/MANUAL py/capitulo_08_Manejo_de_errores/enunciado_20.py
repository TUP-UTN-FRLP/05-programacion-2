# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# ENUNCIADO 20
# Función procesar_operacion(a, b, op) que haga a + b, a - b, a * b
# o a / b según op. Debe manejar: operador inválido (lanzar
# ValueError), división por cero (dejar que suba naturalmente),
# tipos incompatibles (dejar que suba naturalmente). Después llamala
# varias veces desde un bloque try/except que atrape las tres cosas
# por separado.
# -------------------------------------------------------------------------


def procesar_operacion(a, b, op):
    if op == "+":
        return a + b

    if op == "-":
        return a - b

    if op == "*":
        return a * b

    if op == "/":
        return a / b

    raise ValueError(f"Operador desconocido: '{op}'")


pruebas = [
    (10, 5, "+"),
    (10, 0, "/"),
    (10, "cinco", "*"),
    (10, 5, "%")
]

for a, b, op in pruebas:
    # procesar_operacion() puede lanzar ValueError (operador inválido),
    # ZeroDivisionError (b == 0) o TypeError (tipos incompatibles).
    # Cada except captura un error distinto y muestra su propio mensaje.
    try:
        resultado = procesar_operacion(a, b, op)
        print(f"{a} {op} {b} = {resultado}")

    except ValueError as e:
        print(f"Error de valor: {e}")

    except ZeroDivisionError:
        print(f"{a} {op} {b}: no se puede dividir por cero")

    except TypeError as e:
        print(f"Tipos incompatibles: {e}")
