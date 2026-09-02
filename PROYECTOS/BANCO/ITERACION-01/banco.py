"""Proyecto Integrador Banco - Iteracion 1 (implementacion de referencia).

Para que sirve este archivo
---------------------------
Es una version de referencia de la catedra. NO es "la solucion correcta
unica": sirve para que compares tu propio banco.py con una implementacion
posible y revises si cumpliste el objetivo de la iteracion.

Que se puede usar en la Iteracion 1 (y nada mas)
-----------------------------------------------
- clases
- atributos
- metodos
- self
- __init__
- __str__
- parametros y parametros con valor por defecto

Que NO va todavia: validaciones, propiedades (@property), getters/setters,
excepciones, herencia, archivos, bases de datos. Ver ITERACION_01.md.

Idea central de la iteracion
----------------------------
La clase permite A PROPOSITO estados incorrectos: depositar un monto
negativo, extraer mas de lo que hay (saldo negativo), crear una cuenta con
datos vacios o cambiar el saldo "a mano" con ``cuenta.saldo = 99999999``.
Todavia no hay ninguna regla que lo impida; eso se resuelve en la Iteracion 2
con encapsulamiento y validacion.
"""


class Cuenta:
    """Una cuenta bancaria: numero, titular y saldo.

    ``class`` define un molde. Con ese molde despues creamos objetos
    concretos (``cuenta_1``, ``cuenta_2``, ...), cada uno con sus propios
    datos.
    """

    def __init__(self, numero, titular, saldo_inicial=0):
        # __init__ es el CONSTRUCTOR: Python lo ejecuta solo al hacer
        # ``Cuenta(...)``. Sirve para dejar el objeto con sus datos iniciales.
        #
        # ``self`` es el objeto que se esta creando. ``self.numero = numero``
        # guarda el valor recibido DENTRO del objeto (atributo de instancia),
        # asi cada cuenta recuerda lo suyo.
        #
        # ``saldo_inicial=0`` es un parametro con valor por defecto: si al
        # crear la cuenta no se pasa un saldo, arranca en 0.
        #     Cuenta("001-234", "Ana Perez", 1000)  -> saldo 1000
        #     Cuenta("001-235", "Juan Lopez")       -> saldo 0
        self.numero = numero
        self.titular = titular
        self.saldo = saldo_inicial

    def depositar(self, monto):
        """Aumenta el saldo en ``monto``.

        En la Iteracion 1 NO se valida: si ``monto`` es negativo, el saldo
        baja. Eso esta permitido a proposito en esta version.
        """
        self.saldo = self.saldo + monto

    def extraer(self, monto):
        """Disminuye el saldo en ``monto``.

        Tampoco se valida: se puede extraer mas de lo que hay y la cuenta
        queda con saldo negativo. Se resolvera en la proxima iteracion.
        """
        self.saldo = self.saldo - monto

    def __str__(self):
        # __str__ define el texto que se ve al hacer ``print(cuenta)``.
        # ``{:.2f}`` muestra el saldo con 2 decimales (centavos).
        # Ejemplo: Cuenta N° 001-234 - Ana Perez - Saldo: $1300.00
        return "Cuenta N° {} - {} - Saldo: ${:.2f}".format(
            self.numero, self.titular, self.saldo
        )


# Este bloque se ejecuta SOLO cuando corremos el archivo directamente
# (``python banco.py``). Aca abajo va la demostracion pedida por la consigna:
# operaciones validas + comprobacion de las limitaciones actuales.
if __name__ == "__main__":
    # 1) Crear una cuenta con saldo inicial.
    cuenta_1 = Cuenta("001-234", "Ana Perez", 1000)
    # 2) Crear una cuenta sin saldo inicial (usa el valor por defecto 0).
    cuenta_2 = Cuenta("001-235", "Juan Lopez")

    print("Estado inicial:")
    print(f"  {cuenta_1}")
    print(f"  {cuenta_2}")

    # 3) Deposito y 4) extraccion. 5) mostrar antes y despues.
    cuenta_1.depositar(500)
    print(f"\nDespues de depositar 500 : {cuenta_1}")
    cuenta_1.extraer(200)
    print(f"Despues de extraer 200   : {cuenta_1}")

    # ----------------------------------------------------------------------
    # Situaciones incorrectas que ESTA version permite (todavia sin reglas).
    # ----------------------------------------------------------------------
    print("\nLimitaciones de la Iteracion 1 (todo esto hoy se permite):")

    cuenta_1.depositar(-500)
    print(f"  depositar -500      -> saldo ${cuenta_1.saldo:.2f}")

    cuenta_1.extraer(100000)
    print(f"  extraer 100000      -> saldo ${cuenta_1.saldo:.2f} (negativo)")

    cuenta_mala = Cuenta("", "", -1000)
    print(f"  cuenta con datos vacios y saldo negativo -> {cuenta_mala}")

    cuenta_2.saldo = 99999999
    print(f"  asignar saldo a mano -> {cuenta_2}")
