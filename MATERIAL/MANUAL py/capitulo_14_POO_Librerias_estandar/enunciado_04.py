# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------
# Dada una fecha de nacimiento como texto "dd/mm/aaaa", calculá la edad
# exacta en años. Usá datetime.strptime, que es la herramienta del
# capítulo para parsear fechas con formato. Cuidado con el caso de quien
# todavía no cumplió años este año: hay que restarle uno.
# -------------------------------------------------------------------------

from datetime import date, datetime


def calcular_edad(fecha_nacimiento_texto, hoy=None):
    """Calcula la edad en años a partir de una fecha dd/mm/aaaa."""
    nacimiento = datetime.strptime(
        fecha_nacimiento_texto, "%d/%m/%Y"
    ).date()

    if hoy is None:
        hoy = date.today()

    edad = hoy.year - nacimiento.year

    # Comparar (mes, día) como tupla resuelve el caso de borde
    # sin escribir dos condiciones anidadas.
    if (hoy.month, hoy.day) < (nacimiento.month, nacimiento.day):
        edad -= 1

    return edad


if __name__ == "__main__":
    # strptime acepta "5/8/2000" sin cero adelante; date.fromisoformat
    # no lo aceptaría. Por eso conviene la herramienta del capítulo.
    referencia = date(2026, 7, 26)

    for texto in ["15/08/2000", "5/8/2000", "26/07/2000"]:
        edad = calcular_edad(texto, referencia)
        print(f"{texto:>12} -> {edad} años al {referencia}")

    print(f"Edad real hoy: {calcular_edad('15/08/2000')}")
