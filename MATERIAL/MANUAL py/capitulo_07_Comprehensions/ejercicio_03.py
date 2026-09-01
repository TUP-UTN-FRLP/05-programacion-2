# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Ejercicio 3
# Dada una lista de precios [500, 1200, 800, 1500, 950, 2000, 3500],
# generar una lista con los precios en pesos-con-IVA (21%) pero solo
# de los productos que originalmente costaban más de $1000.
# -----------------------------------------------------------------------------


precios = [500, 1200, 800, 1500, 950, 2000, 3500]

# Colección destino = [expresión - ¿Qué hago con los datos? - for elemento in
# colección - ¿De dónde saco los datos? - ¿Que datos quiero?]
# [agregar IVA a todo precio en precios si este es mayor que 1000]
con_iva = [p * 1.21 for p in precios if p > 1000]
print(con_iva)
