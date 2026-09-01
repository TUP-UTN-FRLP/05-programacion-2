# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# ENUNCIADO 4
# Dada la lista list(range(1, 21)), generar una lista con los
# números divisibles por 3 o por 5.
# -----------------------------------------------------------------------------

# -----------------------------------------------------------------------------
# Colección destino: divisibles
# Que tipo de colección destino quiero: lista []
# Cómo guardo los datos: n (el número sin modificar)
# Cómo obtengo los datos: n
# Desde que colección: range(1, 21)
# Filtrado previo: n % 3 == 0 or n % 5 == 0 (divisibles por 3 o por 5)
# -----------------------------------------------------------------------------
divisibles = [n for n in range(1, 21) if n % 3 == 0 or n % 5 == 0]
print(divisibles)
