"""Proyecto Integrador Banco - Iteracion 2 (implementacion de referencia).

Que hay en este archivo
-----------------------
Dos clases que modelan el dominio de un banco chico:

- ``Persona``: el titular de una cuenta (nombre, apellido y DNI).
- ``Cuenta``: un numero de cuenta, un titular (una ``Persona``) y un saldo.

Ideas nuevas de la Iteracion 2 que conviene mirar mientras se lee el codigo:

1. Encapsulamiento: los datos se guardan en atributos que empiezan con dos
   guiones bajos (``self.__saldo``). Python les cambia el nombre por dentro
   ("name mangling"), asi que desde afuera NO se pueden tocar directamente.
2. ``@property``: expone cada atributo privado como si fuera de lectura. Hay
   getter pero no setter, entonces ``cuenta.saldo = 999`` lanza AttributeError.
3. Validacion: antes de guardar un dato se lo pasa por una funcion de
   ``validaciones.py``. Si algo esta mal, se corta con una excepcion:
   - ``TypeError``  -> el tipo del dato no corresponde (ej: un DNI numerico).
   - ``ValueError`` -> el tipo esta bien pero el valor no cumple la regla
     (ej: un DNI de 3 digitos, o extraer mas plata de la que hay).
4. Composicion: una ``Cuenta`` "tiene una" ``Persona``. El constructor exige
   que el titular sea realmente una ``Persona`` y no, por ejemplo, un string.

Lo que NO entra todavia: movimientos, historial, fechas, herencia
(ver ITERACION_02.md).

Este archivo es la referencia de la catedra para verificar que test.py sea
consistente. Cada estudiante escribe su propia version en su rama.
"""

# Un modulo puede importar funciones de otro modulo. Aca traemos solo las
# funciones de validacion que necesitamos, cada una en su propia linea para
# que el import se lea facil y el editor avise si sobra alguna.
from validaciones import (
    validar_dni,
    validar_monto,
    validar_nombre,
    validar_numero_cuenta,
    validar_saldo_inicial,
)


class Persona:
    """Titular de una cuenta: nombre, apellido y DNI, todos de solo lectura.

    Los datos se validan y normalizan una sola vez, en el constructor. A
    partir de ahi el objeto queda "congelado": se pueden leer sus datos pero
    no cambiarlos.
    """

    def __init__(self, nombre, apellido, dni):
        # ``__init__`` es el constructor: se ejecuta al hacer ``Persona(...)``.
        # Cada validar_* devuelve el dato ya limpio (o lanza una excepcion),
        # y recien entonces lo guardamos en el atributo privado.
        self.__nombre = validar_nombre(nombre)
        self.__apellido = validar_nombre(apellido)
        self.__dni = validar_dni(dni)

    # ``@property`` convierte un metodo en un atributo de lectura: se usa como
    # ``persona.nombre`` (sin parentesis). Como no definimos un "setter",
    # intentar ``persona.nombre = "Otra"`` lanza AttributeError.
    @property
    def nombre(self):
        return self.__nombre

    @property
    def apellido(self):
        return self.__apellido

    @property
    def dni(self):
        return self.__dni

    @property
    def nombre_completo(self):
        # Una property tambien sirve para datos calculados: este no se guarda
        # en ningun atributo, se arma cada vez a partir de los otros dos.
        return f"{self.__apellido}, {self.__nombre}"

    def __str__(self):
        # ``__str__`` define el texto que se ve al hacer ``print(persona)`` o
        # ``str(persona)``. Sin esto, print mostraria algo como
        # ``<banco.Persona object at 0x...>``.
        return f"{self.nombre_completo} (DNI {self.__dni})"


class Cuenta:
    """Cuenta bancaria: numero, titular (una ``Persona``) y saldo.

    ``numero`` y ``titular`` no cambian nunca. ``saldo`` solo se modifica
    desde adentro, a traves de ``depositar()`` y ``extraer()``; no hay forma
    de asignarlo "a mano" desde afuera.
    """

    def __init__(self, numero, titular, saldo_inicial=0):
        # ``saldo_inicial=0`` es un parametro con valor por defecto: si al
        # crear la cuenta no se pasa un saldo, arranca en 0.
        self.__numero = validar_numero_cuenta(numero)
        # Composicion + chequeo de tipo: el titular tiene que ser una Persona.
        # Si no lo es, cortamos con TypeError antes de guardar nada.
        if not isinstance(titular, Persona):
            raise TypeError("El titular debe ser una instancia de Persona")
        self.__titular = titular
        self.__saldo = validar_saldo_inicial(saldo_inicial)

    @property
    def numero(self):
        return self.__numero

    @property
    def titular(self):
        return self.__titular

    @property
    def saldo(self):
        return self.__saldo

    def depositar(self, monto):
        """Suma ``monto`` al saldo. El monto debe ser un numero mayor que 0."""
        # validar_monto devuelve el numero si es valido; si no, lanza la
        # excepcion y la linea siguiente nunca se ejecuta (el saldo no cambia).
        monto = validar_monto(monto)
        self.__saldo += monto

    def extraer(self, monto):
        """Resta ``monto`` del saldo si alcanza; si no, lanza ValueError."""
        monto = validar_monto(monto)
        # Regla de negocio: no se puede quedar en negativo. Chequeamos ANTES
        # de tocar el saldo, asi ante un error el saldo queda intacto.
        if monto > self.__saldo:
            raise ValueError("Saldo insuficiente para la extraccion")
        self.__saldo -= monto

    def __str__(self):
        # ``:.2f`` formatea el numero con exactamente 2 decimales (centavos).
        return (
            f"Cuenta N° {self.__numero} - {self.__titular.nombre_completo} "
            f"- Saldo: ${self.__saldo:.2f}"
        )


# ``if __name__ == "__main__":`` -> este bloque corre SOLO si ejecutamos este
# archivo directamente (``python banco.py``). Si otro modulo hace
# ``from banco import Cuenta`` (como test.py), este bloque NO se ejecuta.
# Sirve para tener un pequeño escenario de prueba manual sin ensuciar las
# clases.
# if __name__ == "__main__":
# Fijarse que pasamos los datos "sucios" a proposito ("  ana  ",
# "  pérez ") para ver que Persona los normaliza a "Ana" y "Pérez".
titular = Persona("  ana  ", "  pérez ", "12345678")
cuenta = Cuenta("12345678901234", titular)

cuenta.depositar(1000)
cuenta.depositar(500)
cuenta.extraer(200)
cuenta.depositar(250)
cuenta.extraer(100)
print("Titular:")
print(f"  nombre completo: {titular.nombre_completo}")
print(f"  DNI            : {titular.dni}")
print("Cuenta:")
print(f"  {cuenta}")
print(f"  saldo final    : ${cuenta.saldo:.2f}")
# Cada elemento de la lista es (texto, funcion-sin-argumentos). Usamos
# ``lambda`` para GUARDAR la accion sin ejecutarla todavia: la llamada
# real ocurre mas abajo, dentro del try, cuando escribimos ``accion()``.
# Asi podemos meter en un try/except varias operaciones que sabemos que
# van a fallar, y confirmar que cada una lanza la excepcion esperada.
print("\nSituaciones que ahora se rechazan:")
for descripcion, accion in [
    ("depositar monto negativo", lambda: cuenta.depositar(-500)),
    ("extraer mas que el saldo", lambda: cuenta.extraer(100000)),
    ("cuenta con titular str", lambda: Cuenta("12345678901234",
     "Ana Pérez")),
    ("saldo inicial negativo", lambda: Cuenta("12345678901234", titular,
     -1000)),
    ("asignar saldo directo", lambda: setattr(cuenta, "saldo", 99999999)),
]:
    try:
        accion()
        # Si llegamos aca, la accion NO lanzo excepcion: eso es un fallo,
        # porque esperabamos que el modelo la rechazara.
        print(f"  [FALLO] {descripcion}: no lanzo excepcion")
    except (ValueError, TypeError, AttributeError) as error:
        # ``type(error).__name__`` es el nombre de la clase de la
        # excepcion ("ValueError", "TypeError", ...). Lo mostramos para
        # ver que cada caso falla por el motivo correcto.
        print(f"  [OK] {descripcion}: {type(error).__name__} - {error}")
