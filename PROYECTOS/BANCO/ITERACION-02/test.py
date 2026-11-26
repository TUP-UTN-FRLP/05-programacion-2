"""Suite unica de la Iteracion 2 (contrato tecnico parcial).

Que es este archivo
-------------------
Un conjunto de "tests": funciones cortas que crean objetos y comprueban con
``assert`` que se comportan como esperamos. Es, en la practica, la lista de
requisitos de ``validaciones.py`` y ``banco.py`` escrita en codigo.

En la Iteracion 2 este archivo NO se ejecuta: se lee como referencia del
comportamiento esperado y sus casos se comprueban a mano en el escenario de
banco.py. pytest se empieza a ejecutar en la Iteracion 3, y este mismo archivo
sirve de molde para escribir los tests propios de esa iteracion:

    python -m pip install pytest
    python -m pytest -q

Como leer un test
-----------------
- ``assert <condicion>``: si la condicion es falsa, el test falla.
- ``with pytest.raises(ValueError): ...``: el test PASA solo si el codigo de
  adentro lanza esa excepcion. Sirve para comprobar los casos de error.
- ``@pytest.mark.parametrize("x", [a, b, c])``: corre la misma funcion una vez
  por cada valor de la lista. Es la forma de probar muchos casos sin repetir
  codigo; en el reporte de pytest cuenta como varios tests.

Describe: validaciones, construccion y normalizacion de Persona y Cuenta,
properties de solo lectura, la relacion Cuenta -> Persona y las operaciones
depositar() / extraer(). NO cubre el formato de __str__ ni la salida del
escenario de banco.py: eso sigue siendo responsabilidad del estudiante.
"""

import pytest

# Importamos lo que vamos a testear. Si banco.py o validaciones.py tienen un
# error de sintaxis o les falta algo, este import falla y no corre ningun test.
from banco import Cuenta, Persona
from validaciones import (
    validar_dni,
    validar_monto,
    validar_nombre,
    validar_numero_cuenta,
    validar_saldo_inicial,
)

# Constante compartida: un numero de cuenta valido (14 digitos). Le ponemos
# nombre para no repetir el literal en cada test y para que se lea que "es
# valido".
NUMERO_VALIDO = "12345678901234"


def crear_titular():
    """Devuelve una Persona valida lista para usar como titular.

    Varios tests necesitan "una Persona cualquiera pero correcta". En vez de
    repetir estos datos, los centralizamos aca: si cambia la forma de crear
    una Persona, se toca un solo lugar.
    """
    return Persona("Ana", "Pérez", "12345678")


# --------------------------------------------------------------------------- #
# validaciones.py
# --------------------------------------------------------------------------- #
# Estas funciones reciben un dato "crudo", devuelven el dato ya normalizado si
# es valido, y lanzan una excepcion si no lo es:
#   - TypeError  -> el tipo no corresponde (ej: pasar un int donde va un str).
#   - ValueError -> el tipo esta bien pero el valor no cumple la regla.

def test_validar_nombre_limpia_y_normaliza():
    # Saca espacios de los bordes, colapsa los internos y aplica title().
    assert validar_nombre("  ana   maría ") == "Ana María"


def test_validar_nombre_normaliza_espacios_internos():
    assert validar_nombre("de   la   cruz") == "De La Cruz"


def test_validar_nombre_admite_guion_y_apostrofo():
    # Apellidos como "O'Brien-Smith" son validos: se permiten ' y -.
    assert validar_nombre("o'brien-smith") == "O'Brien-Smith"


@pytest.mark.parametrize("valor", ["", "   ", "Ana_123", "Ana@Pérez", "Ana 2"])
def test_validar_nombre_rechaza_valores_invalidos(valor):
    # Vacio, solo espacios, digitos o simbolos raros -> ValueError.
    with pytest.raises(ValueError):
        validar_nombre(valor)


def test_validar_nombre_rechaza_tipo_incorrecto():
    # 123 es un int, no un str: el error es de TIPO, no de valor.
    with pytest.raises(TypeError):
        validar_nombre(123)


@pytest.mark.parametrize("dni", ["1234567", "12345678", "01234567"])
def test_validar_dni_acepta_7_u_8_digitos(dni):
    # El DNI se guarda como str (puede empezar con 0) y se devuelve igual.
    assert validar_dni(dni) == dni


@pytest.mark.parametrize("dni", ["123456", "123456789", "12A45678",
                         "12.345.678", ""])
def test_validar_dni_rechaza_formato_invalido(dni):
    # Es un str, pero no son 7 u 8 digitos limpios -> ValueError.
    with pytest.raises(ValueError):
        validar_dni(dni)


def test_validar_dni_rechaza_tipo_incorrecto():
    # 12345678 sin comillas es un int -> TypeError (aunque "parezca" un DNI).
    with pytest.raises(TypeError):
        validar_dni(12345678)


def test_validar_numero_cuenta_acepta_14_digitos():
    assert validar_numero_cuenta(NUMERO_VALIDO) == NUMERO_VALIDO


@pytest.mark.parametrize(
    "numero", ["", "123", "1234567890123A", "1234-5678901234",
               "123456789012345"]
)
def test_validar_numero_cuenta_rechaza_formato_invalido(numero):
    # Menos/mas de 14, con letras o con guiones -> ValueError.
    with pytest.raises(ValueError):
        validar_numero_cuenta(numero)


def test_validar_numero_cuenta_rechaza_tipo_incorrecto():
    with pytest.raises(TypeError):
        validar_numero_cuenta(12345678901234)


def test_validar_saldo_inicial_acepta_cero_y_positivos():
    # El saldo inicial puede ser 0 y puede tener decimales.
    assert validar_saldo_inicial(0) == 0
    assert validar_saldo_inicial(1500.50) == 1500.50


def test_validar_saldo_inicial_rechaza_negativo():
    with pytest.raises(ValueError):
        validar_saldo_inicial(-1)


@pytest.mark.parametrize("valor", ["1000", None, True])
def test_validar_saldo_inicial_rechaza_tipo_incorrecto(valor):
    # Ojo con True: en Python bool es subtipo de int, pero un saldo NO es un
    # booleano, asi que la validacion lo rechaza igual -> TypeError.
    with pytest.raises(TypeError):
        validar_saldo_inicial(valor)


@pytest.mark.parametrize("monto", [1, 100, 10.50])
def test_validar_monto_acepta_positivos(monto):
    assert validar_monto(monto) == monto


@pytest.mark.parametrize("monto", [0, -1, -10.50])
def test_validar_monto_rechaza_cero_y_negativos(monto):
    # Un movimiento de 0 o negativo no tiene sentido -> ValueError.
    with pytest.raises(ValueError):
        validar_monto(monto)


@pytest.mark.parametrize("valor", ["100", None, True])
def test_validar_monto_rechaza_tipo_incorrecto(valor):
    with pytest.raises(TypeError):
        validar_monto(valor)


# --------------------------------------------------------------------------- #
# Persona
# --------------------------------------------------------------------------- #
# Persona valida y normaliza sus datos en el constructor, y despues los expone
# como properties de SOLO LECTURA.

def test_crear_persona_valida():
    persona = Persona("  ana  ", "  pérez ", "12345678")

    # Los datos entraron "sucios" y salen normalizados por las properties.
    assert persona.nombre == "Ana"
    assert persona.apellido == "Pérez"
    assert persona.dni == "12345678"
    # nombre_completo es una property calculada: "Apellido, Nombre".
    assert persona.nombre_completo == "Pérez, Ana"


def test_persona_normaliza_espacios_internos():
    persona = Persona("ana   maría", "de   la   cruz", "12345678")

    assert persona.nombre == "Ana María"
    assert persona.apellido == "De La Cruz"


@pytest.mark.parametrize(
    "nombre, apellido, dni",
    [
        ("", "Pérez", "12345678"),
        ("Ana", "", "12345678"),
        ("Ana", "Pérez", "1234"),
        ("Ana", "Pérez", "12A45678"),
    ],
)
def test_persona_rechaza_datos_invalidos(nombre, apellido, dni):
    # Si CUALQUIER dato es invalido, ni siquiera se llega a crear la Persona.
    with pytest.raises((ValueError, TypeError)):
        Persona(nombre, apellido, dni)


def test_persona_rechaza_dni_numerico():
    with pytest.raises(TypeError):
        Persona("Ana", "Pérez", 12345678)


def test_propiedades_de_persona_son_solo_lectura():
    persona = crear_titular()

    # No hay "setter": asignar sobre la property lanza AttributeError. Asi el
    # objeto no se puede modificar despues de creado.
    with pytest.raises(AttributeError):
        persona.nombre = "Otra"
    with pytest.raises(AttributeError):
        persona.apellido = "Otro"
    with pytest.raises(AttributeError):
        persona.dni = "87654321"


# --------------------------------------------------------------------------- #
# Cuenta - construccion
# --------------------------------------------------------------------------- #
# Al crear una Cuenta se valida el numero, se exige que el titular sea una
# Persona (composicion) y se valida el saldo inicial.

def test_crear_cuenta_con_saldo_cero_por_defecto():
    titular = crear_titular()
    cuenta = Cuenta(NUMERO_VALIDO, titular)

    assert cuenta.numero == NUMERO_VALIDO
    # ``is`` compara identidad: la cuenta guarda EL MISMO objeto Persona, no
    # una copia.
    assert cuenta.titular is titular
    # Sin pasar saldo_inicial, arranca en 0 (parametro con valor por defecto).
    assert cuenta.saldo == 0


def test_crear_cuenta_con_saldo_inicial():
    cuenta = Cuenta(NUMERO_VALIDO, crear_titular(), 2500.50)

    assert cuenta.saldo == 2500.50


@pytest.mark.parametrize("titular", ["Ana Pérez", None, 123])
def test_cuenta_requiere_persona_como_titular(titular):
    # Un string, None o un numero no son una Persona -> TypeError.
    with pytest.raises(TypeError):
        Cuenta(NUMERO_VALIDO, titular)


@pytest.mark.parametrize("numero", ["", "123", "1234567890123A",
                         "1234-5678901234"])
def test_cuenta_rechaza_numero_invalido(numero):
    with pytest.raises(ValueError):
        Cuenta(numero, crear_titular())


def test_cuenta_rechaza_numero_no_str():
    with pytest.raises(TypeError):
        Cuenta(12345678901234, crear_titular())


def test_cuenta_rechaza_saldo_inicial_negativo():
    with pytest.raises(ValueError):
        Cuenta(NUMERO_VALIDO, crear_titular(), -1)


@pytest.mark.parametrize("saldo", ["1000", True])
def test_cuenta_rechaza_saldo_inicial_no_numerico(saldo):
    with pytest.raises(TypeError):
        Cuenta(NUMERO_VALIDO, crear_titular(), saldo)


def test_propiedades_de_cuenta_son_solo_lectura():
    cuenta = Cuenta(NUMERO_VALIDO, crear_titular(), 1000)

    # numero, titular y saldo se leen pero no se asignan desde afuera. El
    # saldo solo cambia via depositar() / extraer().
    with pytest.raises(AttributeError):
        cuenta.numero = "99999999999999"
    with pytest.raises(AttributeError):
        cuenta.titular = crear_titular()
    with pytest.raises(AttributeError):
        cuenta.saldo = 999999


# --------------------------------------------------------------------------- #
# Cuenta - operaciones
# --------------------------------------------------------------------------- #
# depositar() suma y extraer() resta, siempre validando el monto. Regla clave:
# si la operacion es invalida, el saldo NO se toca.

def test_depositar_aumenta_el_saldo():
    cuenta = Cuenta(NUMERO_VALIDO, crear_titular(), 100)

    cuenta.depositar(50)

    assert cuenta.saldo == 150


@pytest.mark.parametrize("monto", [0, -1])
def test_depositar_rechaza_monto_no_positivo_sin_cambiar_saldo(monto):
    cuenta = Cuenta(NUMERO_VALIDO, crear_titular(), 100)

    with pytest.raises(ValueError):
        cuenta.depositar(monto)
    # Despues del error, el saldo sigue siendo el original.
    assert cuenta.saldo == 100


def test_depositar_rechaza_monto_no_numerico():
    cuenta = Cuenta(NUMERO_VALIDO, crear_titular(), 100)

    with pytest.raises(TypeError):
        cuenta.depositar("50")
    assert cuenta.saldo == 100


def test_extraer_disminuye_el_saldo():
    cuenta = Cuenta(NUMERO_VALIDO, crear_titular(), 100)

    cuenta.extraer(40)

    assert cuenta.saldo == 60


def test_extraer_rechaza_saldo_insuficiente_sin_cambiar_saldo():
    cuenta = Cuenta(NUMERO_VALIDO, crear_titular(), 100)

    # No se puede extraer mas de lo que hay, y el intento no descuenta nada.
    with pytest.raises(ValueError):
        cuenta.extraer(150)
    assert cuenta.saldo == 100


@pytest.mark.parametrize("monto", [0, -20])
def test_extraer_rechaza_monto_no_positivo(monto):
    cuenta = Cuenta(NUMERO_VALIDO, crear_titular(), 100)

    with pytest.raises(ValueError):
        cuenta.extraer(monto)
    assert cuenta.saldo == 100


def test_extraer_rechaza_monto_no_numerico():
    cuenta = Cuenta(NUMERO_VALIDO, crear_titular(), 100)

    with pytest.raises(TypeError):
        cuenta.extraer("40")
