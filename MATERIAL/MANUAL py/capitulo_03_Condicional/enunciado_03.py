# ============================================================
# Enunciado 3:
# Un minorista aplica un 10% de descuento si la compra supera los 1000 pesos.
# Pedir el total de la compra y mostrar cuánto debe pagar final.
#
# PREGUNTA 1: ¿Qué pasa si la compra es exactamente 1000 pesos?
# PREGUNTA 2: ¿Cómo mejorar el código si se ingresa valor negativo o no
# numérico?
# ============================================================

respuesta = input("Total compra: ")

if not respuesta.isdigit():
    print("Error: Debe ingresar solo números.")
else:
    compra = float(respuesta)
    if compra < 0:
        print("Error: El valor de la compra no puede ser negativo.")
    elif compra > 1000:
        compra = compra - (compra * 0.10)
        print(f"Debe pagar: ${compra:.2f}")
    else:
        print(f"Debe pagar: ${compra:.2f}")
