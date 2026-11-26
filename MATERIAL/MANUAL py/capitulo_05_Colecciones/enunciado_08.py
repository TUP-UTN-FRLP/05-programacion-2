# -*- coding: utf-8 -*-
# ----------------------------------------------------------
# Enunciado 8:
# Un profesor tiene dos sets: alumnos aprobados en el primer
# parcial y en el segundo.
# También conoce el total de inscriptos.
# Mostrar:
# - Quiénes aprobaron ambos.
# - Quiénes aprobaron solo uno.
# - Quiénes no aprobaron ninguno.
# ----------------------------------------------------------

# Alumnos que aprobaron el primer parcial
primer_parcial = {"Ana", "Juan", "Pedro", "Lucía"}

# Alumnos que aprobaron el segundo parcial
segundo_parcial = {"Juan", "Pedro", "Diego", "María"}

# Total de alumnos inscriptos
total = {"Ana", "Juan", "Pedro", "Lucía", "Diego", "María", "Sofía"}

# Intersección: alumnos que aprobaron ambos parciales
ambos = primer_parcial & segundo_parcial

# Unión: todos los que aprobaron al menos un parcial.
# Luego quitamos los que aprobaron ambos.
solo_uno = (primer_parcial | segundo_parcial) - ambos

# Quitamos del total a todos los que aprobaron algún parcial
ninguno = total - (primer_parcial | segundo_parcial)

# Mostrar los resultados
print(f"Aprobaron ambos: {ambos}")
print(f"Aprobaron solo uno: {solo_uno}")
print(f"No aprobaron ninguno: {ninguno}")
