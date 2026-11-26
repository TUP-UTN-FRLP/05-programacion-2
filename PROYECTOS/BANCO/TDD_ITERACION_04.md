# Contrato de comportamiento y guía de pruebas — Iteración 4

> **Recordatorio:** `test.py` ya se ejecuta desde la Iteración 3 y pasarlo es
> condición de entrega. Lo nuevo acá es la **organización**: las pruebas propias
> se parten en varios archivos dentro de `tests/`, con `conftest.py` para las
> fixtures compartidas, y se mide cobertura.

## Índice

1. Puesta en marcha
2. Anatomía de un test
3. El ciclo TDD
4. Fixtures
5. Pruebas parametrizadas
6. Pruebas de excepciones
7. Contrato de `errores.py`
8. Contrato de `Movimiento`
9. Contrato del historial y la baja lógica
10. Contrato del CBU
11. Contrato de `Banco`
12. Contrato de la transferencia atómica
13. Qué tests hay que escribir
14. Cobertura
15. Errores frecuentes

---

## 1. Puesta en marcha

```bash
python -m pip install pytest
python -m pytest -q
```

```text
tests/
    __init__.py
    test_movimientos.py
    test_banco.py
    test_transferencias.py
    conftest.py
pytest.ini
```

```ini
[pytest]
python_files = test.py test_*.py
testpaths = . tests
```

### Comandos de uso diario

| Comando | Para qué |
| --- | --- |
| `python -m pytest -q` | ejecutar todo, salida corta |
| `python -m pytest -v` | ver el nombre de cada test |
| `python -m pytest -x` | frenar en el primer fallo |
| `python -m pytest --lf` | reejecutar solo los que fallaron |
| `python -m pytest -k "transferencia"` | filtrar por nombre |
| `python -m pytest tests/test_banco.py::test_abrir_cuenta` | un test puntual |

---

## 2. Anatomía de un test

Una función que empieza con `test_`, no devuelve nada y verifica con `assert`.
Estructura **Arrange–Act–Assert**:

```python
def test_deposito_aumenta_el_saldo():
    # Arrange
    titular = PersonaFisica("Ana", "Perez", "12345678", 30)
    cuenta = CuentaAhorro("00000123456789", titular, 1000)

    # Act
    cuenta.depositar(500)

    # Assert
    assert cuenta.saldo == 1500
```

Reglas obligatorias:

- **un comportamiento por test**; si el nombre necesita un "y", son dos tests;
- el nombre describe el comportamiento, no la implementación:
  `test_extraer_sin_fondos_no_modifica_el_saldo`, no `test_extraer_2`;
- sin `print()`: si un test necesita `print()` para entenderse, le falta un
  `assert`;
- sin `if` ni `for` que decidan qué verificar (para eso está `parametrize`);
- los tests no dependen del orden de ejecución ni comparten estado.

---

## 3. El ciclo TDD

Para cada método nuevo de `Banco`:

```text
1. ROJO      escribir el test; ejecutarlo; debe fallar
2. VERDE     escribir el código mínimo para que pase
3. REFACTOR  mejorar el código con la red de tests puesta
```

El paso 1 no es opcional: **un test que nunca se vio fallar no prueba nada**.
Un test mal escrito puede pasar por accidente —por ejemplo, si el nombre del
método está mal tipeado y la excepción esperada es `AttributeError`.

### Evidencia en los commits

En el historial de la rama individual debe verse al menos **tres veces** el par:

```text
Agrega test de cierre de cuenta con saldo     (rojo)
Implementa cierre de cuenta con validacion    (verde)
```

Ese par, en ese orden, es la prueba de que se aplicó TDD y no se escribieron los
tests al final.

---

## 4. Fixtures

En `tests/conftest.py` (pytest lo descubre solo, no se importa):

```python
import pytest

from banco import Banco
from personas import PersonaFisica, PersonaJuridica


@pytest.fixture
def titular():
    return PersonaFisica("Ana", "Perez", "12345678", 30)


@pytest.fixture
def empresa():
    return PersonaJuridica("Distribuidora S.A.", "30712345671")


@pytest.fixture
def banco():
    return Banco("Banco UTN")


@pytest.fixture
def banco_con_cuentas(banco, titular, empresa):
    """Una caja de ahorro con $1000 y una corriente con $1000 y $5000 de giro."""
    banco.abrir_cuenta("AHORRO", titular, 1000)
    banco.abrir_cuenta("CORRIENTE", empresa, 1000, limite_descubierto=5000)
    return banco
```

Uso:

```python
def test_abrir_cuenta_la_registra(banco, titular):
    cuenta = banco.abrir_cuenta("AHORRO", titular)

    assert banco.buscar_cuenta(cuenta.cbu) is cuenta
```

Puntos importantes:

- cada test recibe instancias **nuevas**: las fixtures se reejecutan por test,
  así no se contamina el estado;
- una fixture puede depender de otra;
- si el contador de números de cuenta es un atributo de clase, agregar una
  fixture con `autouse=True` que lo reinicie antes de cada test. Si no, los
  tests pasan sueltos y fallan juntos.

---

## 5. Pruebas parametrizadas

```python
@pytest.mark.parametrize("cuit_invalido", [
    "30712345670",     # verificador incorrecto
    "3071234567",      # 10 dígitos
    "307123456712",    # 12 dígitos
    "30-71234567-1",   # con guiones
    "3071234567a",     # con una letra
    "",
])
def test_cuit_invalido_es_rechazado(cuit_invalido):
    with pytest.raises(CuitInvalidoError):
        PersonaJuridica("Distribuidora S.A.", cuit_invalido)
```

`pytest` cuenta esto como seis tests: si falla uno, se ve exactamente cuál.

Con varios parámetros:

```python
@pytest.mark.parametrize("saldo, limite, monto, permitido", [
    (1000, 0, 1000, True),
    (1000, 0, 1000.01, False),
    (1000, 5000, 6000, True),
    (1000, 5000, 6000.01, False),
    (0, 5000, 5000, True),
])
def test_limite_de_extraccion(titular, saldo, limite, monto, permitido):
    ...
```

---

## 6. Pruebas de excepciones

```python
def test_extraer_sin_fondos(banco_con_cuentas):
    cbu = banco_con_cuentas.listar_cuentas_activas()[0].cbu

    with pytest.raises(SaldoInsuficienteError):
        banco_con_cuentas.extraer(cbu, 99999)
```

### Verificar el mensaje

```python
with pytest.raises(SaldoInsuficienteError, match="insuficiente"):
    ...
```

`match` recibe una expresión regular que se busca en el mensaje. Usar un
fragmento estable, no el texto completo con importes formateados.

### Verificar los atributos de la excepción

```python
with pytest.raises(SaldoInsuficienteError) as info:
    cuenta.extraer(5000)

assert info.value.disponible == 1000
assert info.value.solicitado == 5000
```

### Verificar que el estado no cambió

Un test de excepción está **incompleto** si solo verifica que la excepción se
lanzó:

```python
def test_extraccion_fallida_no_deja_rastro(cuenta):
    saldo_previo = cuenta.saldo
    movimientos_previos = len(cuenta.historial())

    with pytest.raises(SaldoInsuficienteError):
        cuenta.extraer(99999)

    assert cuenta.saldo == saldo_previo
    assert len(cuenta.historial()) == movimientos_previos
```

---

## 7. Contrato de `errores.py`

| Caso | Esperado |
| --- | --- |
| `issubclass(ErrorDeValidacion, BancoError)` | `True` |
| `issubclass(ErrorDeValidacion, ValueError)` | `True` |
| `issubclass(ErrorDeTipo, TypeError)` | `True` |
| `issubclass(MontoInvalidoError, ErrorDeValidacion)` | `True` |
| `issubclass(LimiteDescubiertoExcedidoError, SaldoInsuficienteError)` | `True` |
| `issubclass(SaldoInsuficienteError, ValueError)` | `False` — es error de operación, no de validación |
| toda excepción del sistema | hereda de `BancoError` |
| `str(error)` | no vacío |

Test de compatibilidad hacia atrás (obligatorio):

```python
def test_los_errores_de_validacion_siguen_siendo_value_error(cuenta):
    with pytest.raises(ValueError):
        cuenta.depositar(-100)
```

---

## 8. Contrato de `Movimiento`

| Caso | Esperado |
| --- | --- |
| `Movimiento.TIPOS` | tupla con los tipos permitidos |
| `movimiento.tipo` / `monto` / `saldo_posterior` | los valores recibidos |
| `movimiento.saldo_posterior` | puede ser negativo |
| `movimiento.fecha_hora` | `datetime` con `tzinfo`, cercano a `now()` en zona argentina |
| `Movimiento("RETIRO", 100, 0)` | `ErrorDeValidacion` |
| `Movimiento("DEPOSITO", 0, 0)` | `MontoInvalidoError` |
| `Movimiento("DEPOSITO", -100, 0)` | `MontoInvalidoError` |
| `Movimiento("DEPOSITO", True, 0)` | `ErrorDeTipo` |
| `movimiento.monto = 999` | `AttributeError` |
| `Movimiento(...)` | no recibe `fecha_hora` por parámetro |

### La hora es la de la Argentina

`Movimiento` fija la fecha con
`datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))`, no con
`datetime.now()` a secas. Consecuencias verificables:

| Caso | Esperado |
| --- | --- |
| `movimiento.fecha_hora.tzinfo` | no es `None` |
| `movimiento.fecha_hora.utcoffset()` | `timedelta(hours=-3)` |
| dos movimientos creados en la misma operación | fechas coherentes con el reloj de Buenos Aires |

El *offset* es −3 h todo el año: la Argentina no aplica horario de verano desde
2009. El test no debe comparar contra `datetime.now()` local del runner de CI
(que corre en UTC): se compara contra
`datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))`.

---

## 9. Contrato del historial y la baja lógica

| Caso | Esperado |
| --- | --- |
| cuenta recién creada con saldo `0` | `historial() == []` |
| cuenta creada con saldo inicial `> 0` | un movimiento `"APERTURA"` |
| `depositar(monto)` | agrega **un** movimiento `"DEPOSITO"` con `saldo_posterior` correcto |
| `extraer(monto)` | agrega un movimiento `"EXTRACCION"` |
| `liquidar_interes()` con saldo `> 0` | agrega `"INTERES"` |
| `liquidar_interes()` con saldo `0` | no agrega nada |
| `cobrar_mantenimiento()` | agrega `"MANTENIMIENTO"` |
| `historial()` | devuelve los movimientos en orden cronológico |
| `cuenta.historial().clear()` | no vacía el historial real |
| `cuenta.activa` | `True` al crear; property de solo lectura |
| `cuenta.activa = False` | `AttributeError` |
| `cerrar()` con saldo `0` | `activa` pasa a `False`, agrega `"CIERRE"` |
| `cerrar()` con saldo `> 0` o `< 0` | `CuentaConSaldoError`; sigue activa |
| `cerrar()` dos veces | `CuentaInactivaError` |
| `depositar()` / `extraer()` sobre cuenta cerrada | `CuentaInactivaError`, saldo sin cambios |
| `historial()` de una cuenta cerrada | sigue devolviendo todos los movimientos |

---

## 10. Contrato del CBU

### Cómo se arma el CBU en la Argentina

El CBU tiene 22 dígitos, repartidos en dos bloques con un dígito verificador
propio cada uno:

```text
bloque 1 (8):  EEE  SSSS  V1        bloque 2 (14):  CCCCCCCCCCCCC  V2
               285  0100   6                        0000000000001   7
               ^^^  ^^^^   ^                        ^^^^^^^^^^^^^   ^
               ent. suc.   dv1                      cuenta (13)     dv2
```

Los dos verificadores se calculan igual: se multiplica cada dígito por su peso,
se suman los productos y

```text
dv = (10 - (suma % 10)) % 10
```

- **Bloque 1** — pesos `7 1 3 9 7 1 3` sobre los primeros 7 dígitos
  (entidad + sucursal).
- **Bloque 2** — pesos `3 9 7 1 3 9 7 1 3 9 7 1 3` sobre los primeros 13
  dígitos (el número de cuenta).

Ejemplo del bloque 1 con `ENTIDAD = "285"` y `SUCURSAL = "0100"`:

```text
dígitos    2   8   5   0   1   0   0
pesos      7   1   3   9   7   1   3
producto  14   8  15   0   7   0   0   ->  suma = 44
dv = (10 - (44 % 10)) % 10 = (10 - 4) % 10 = 6   ->  bloque 1 = "28501006"
```

Como la entidad y la sucursal son constantes en este proyecto, **el bloque 1 es
siempre `"28501006"`**. Lo único que cambia entre una cuenta y otra es el
bloque 2, que depende del número de cuenta de 13 dígitos.

### Casos

| Caso | Esperado |
| --- | --- |
| `validar_cbu("2850100...")` con ambos verificadores correctos | devuelve el `str` |
| CBU de 21 o 23 dígitos | `CbuInvalidoError` |
| CBU con letras o guiones | `CbuInvalidoError` |
| CBU con el verificador del bloque 1 mal | `CbuInvalidoError` |
| CBU con el verificador del bloque 2 mal | `CbuInvalidoError` |
| `validar_cbu(2850100...)` (`int`) | `ErrorDeTipo` |
| `Banco.generar_numero_cuenta()` | `str` de 14 dígitos |
| `Banco.generar_cbu(numero)` | `str` de 22 dígitos que pasa `validar_cbu` |
| dos aperturas seguidas | CBU distintos |
| 100 aperturas | 100 CBU distintos, todos válidos |
| números de cuenta de las iteraciones anteriores | siguen pasando `validar_numero_cuenta` |

La última fila es la comprobación de la decisión de compatibilidad: si
`validar_numero_cuenta` empezara a exigir el dígito verificador, los datos de
prueba viejos dejarían de servir.

---

## 11. Contrato de `Banco`

### Construcción

| Caso | Esperado |
| --- | --- |
| `Banco("Banco UTN")` | `len(banco) == 0`, `listar_cuentas_activas() == []` |
| `Banco("")` / `Banco("   ")` | `ErrorDeValidacion` |
| `Banco(123)` | `ErrorDeTipo` |
| `banco.nombre` | property de solo lectura |

### ABM

| Caso | Esperado |
| --- | --- |
| `abrir_cuenta("AHORRO", titular)` | devuelve una `CuentaAhorro` con saldo `0` |
| `abrir_cuenta("CORRIENTE", titular, 0, limite_descubierto=5000)` | devuelve una `CuentaCorriente` con ese límite |
| `abrir_cuenta("AHORRO", titular, 0, limite_descubierto=5000)` | `ErrorDeValidacion` |
| `abrir_cuenta("PLAZO_FIJO", titular)` | `ErrorDeValidacion` |
| `abrir_cuenta("AHORRO", "Ana Perez")` | `ErrorDeTipo` |
| cuenta creada | `cuenta.titular is titular` (el mismo objeto, no una copia) |
| `buscar_cuenta(cbu)` inexistente | `CuentaInexistenteError` |
| `buscar_cuenta(cbu)` existente | devuelve **el mismo objeto** (`is`) |
| `listar_cuentas_activas()` | no incluye las cerradas |
| `listar_cuentas()` | incluye las cerradas |
| `listar_cuentas_activas().clear()` | no vacía el registro interno |
| `cerrar_cuenta(cbu)` con saldo `0` | la cuenta sigue en `listar_cuentas()`, no en las activas |
| `cerrar_cuenta(cbu)` con saldo | `CuentaConSaldoError` |
| `cerrar_cuenta(cbu)` inexistente | `CuentaInexistenteError` |

### Operaciones

| Caso | Esperado |
| --- | --- |
| `depositar(cbu, monto)` | el saldo aumenta; hay un movimiento nuevo |
| `extraer(cbu, monto)` sin fondos | `SaldoInsuficienteError`; saldo intacto |
| `historial_de(cbu)` | lista de `Movimiento` en orden |
| `total_depositado()` | suma de los saldos, incluidos los negativos |
| `len(banco)` | cantidad de cuentas **activas** |
| `cbu in banco` | `True` si la cuenta existe |
| `for cuenta in banco` | recorre las activas |
| `str(banco)` | incluye el nombre y la cantidad de cuentas |

---

## 12. Contrato de la transferencia atómica

Estos son los casos que hay que probar sí o sí.

| Caso | Esperado |
| --- | --- |
| transferencia válida | origen baja `monto`, destino sube `monto` |
| transferencia válida | origen registra `"TRANSFERENCIA_SALIDA"`, destino `"TRANSFERENCIA_ENTRADA"` |
| **suma de los dos saldos** | idéntica antes y después |
| origen sin fondos | `SaldoInsuficienteError` y **el destino no recibe nada** |
| origen sin fondos | el historial del destino no cambia |
| CBU de destino inexistente | `CuentaInexistenteError`; el origen no cambia |
| CBU de origen inexistente | `CuentaInexistenteError`; nada cambia |
| origen igual a destino | `TransferenciaInvalidaError`; el saldo no se duplica |
| monto `<= 0` o no numérico | `MontoInvalidoError` / `ErrorDeTipo`; nada cambia |
| cuenta origen o destino cerrada | `CuentaInactivaError`; nada cambia |
| ahorro → corriente y corriente → ahorro | ambas combinaciones funcionan |
| corriente en descubierto → ahorro | permitido si no supera el límite |

Test modelo:

```python
def test_transferencia_fallida_no_acredita_en_el_destino(banco_con_cuentas):
    origen, destino = banco_con_cuentas.listar_cuentas_activas()
    saldo_origen = origen.saldo
    saldo_destino = destino.saldo

    with pytest.raises(SaldoInsuficienteError):
        banco_con_cuentas.transferir(origen.cbu, destino.cbu, 999_999)

    assert origen.saldo == saldo_origen
    assert destino.saldo == saldo_destino
    assert len(destino.historial()) == 1      # solo la apertura
```

---

## 13. Qué tests hay que escribir

Cada estudiante entrega **al menos 12 tests propios**:

| Archivo | Mínimo | Contenido |
| --- | --- | --- |
| `tests/test_movimientos.py` | 3 | tipos válidos e inválidos, inmutabilidad, historial |
| `tests/test_banco.py` | 6 | ABM, tipos de cuenta, baja lógica, CBU generado |
| `tests/test_transferencias.py` | 3 | caso feliz, conservación de la suma, fallo sin efectos |

Al menos uno debe usar `parametrize`, y al menos uno debe verificar que **un
error no dejó efectos parciales**.

No cuentan para el mínimo: tests copiados de `test.py`, tests sin `assert`, o
tests que solo verifican que un método existe.

---

## 14. Cobertura (optativo, recomendado)

```bash
python -m pip install pytest-cov
python -m pytest --cov=banco --cov=cuentas --cov=personas --cov=movimientos \
                 --cov=validaciones --cov-report=term-missing
```

La columna `Missing` muestra las líneas que ningún test ejecuta: es la forma más
rápida de encontrar ramas de error nunca probadas.

Advertencia: la cobertura mide **qué se ejecutó**, no **qué se verificó**. Un
test sin `assert` cubre líneas y no prueba nada. Sirve para encontrar huecos, no
como nota.

Referencia razonable: 80 % en los módulos de dominio. `main.py` queda afuera.

---

## 15. Errores frecuentes

| Síntoma | Causa habitual | Solución |
| --- | --- | --- |
| `ModuleNotFoundError: No module named 'banco'` | se ejecutó `pytest` en vez de `python -m pytest` | usar `python -m pytest` desde la raíz |
| `ImportError: cannot import name ...` circular | `cuentas.py` importa `banco.py` | revisar la dirección de las dependencias |
| `test.py` no se ejecuta | falta `python_files` en `pytest.ini` | agregar el `pytest.ini` de la sección 1 |
| un test pasa siempre | falta el `assert`, o el `raises` envuelve código que ya fallaba antes | verlo fallar primero |
| tests que fallan según el orden | estado compartido (atributo de clase mutable, contador global) | reiniciarlo en una fixture `autouse` |
| `pytest.raises` no atrapa nada | se esperaba `ValueError` y ahora se lanza un error propio que no hereda de él | revisar la jerarquía |
| la transferencia "funciona" pero el destino cobra dos veces | se depositó antes de extraer y además se registró aparte | revisar el orden de los pasos |
| `__pycache__/` o `.pytest_cache/` versionados | `.gitignore` incompleto | `git rm -r --cached` y actualizar |
