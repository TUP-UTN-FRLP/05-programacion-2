# Guía para desarrollar los tests — Iteración 4

> **`test.py` ya se ejecuta desde la Iteración 3** y que pase es
> condición de entrega. El archivo de la cátedra **no se toca**. Lo
> nuevo acá: tus pruebas dejan de vivir en un solo archivo y pasan a
> `tests/`, con `conftest.py` y cobertura.

Documento hermano: `TDD_ITERACION_04.md` (el contrato). De la
Iteración 3 ya traés `assert`, fixture, `pytest.raises`, `parametrize`
y `pytest.ini` (`GUIA_TESTS_ITERACION_03.md`); acá se suma la
organización en varios archivos.

---

## 1. Instalar y correr

```bash
python -m pip install pytest
python -m pytest -q
```

Siempre con `python -m pytest`, **no** `pytest` a secas: el `-m` mete
la carpeta actual en el `sys.path`, y sin eso los `from banco import
...` de la suite no resuelven.

Salida esperada: una línea de puntos y `NNN passed`. Si algo falla,
`pytest` te muestra el archivo, la línea, el `assert` que cortó y los
valores reales.

Comandos que vas a usar:

| Comando | Para qué |
| --- | --- |
| `python -m pytest -q` | toda la suite, salida corta |
| `python -m pytest tests/test_movimientos.py` | un solo archivo |
| `python -m pytest -k transferencia` | los tests cuyo nombre contiene "transferencia" |
| `python -m pytest -x` | frená en el primer fallo |
| `python -m pytest --lf` | corré solo los que fallaron la vez pasada |
| `python -m pytest -q -v` | mostrá el nombre de cada caso |

---

## 2. `pytest.ini` — por qué hace falta y qué dice cada línea

Va en la raíz de la carpeta de la iteración, al lado de `banco.py`.

```ini
[pytest]
python_files = test.py test_*.py
testpaths = . tests
addopts = -q
```

- **`python_files`**: qué archivos son suites. Por defecto `pytest`
  toma solo `test_*.py` y `*_test.py`. El archivo de la cátedra se
  llama `test.py` a secas, así que hay que nombrarlo explícitamente.
  Tus archivos en `tests/` sí siguen la convención `test_*.py`.
- **`testpaths`**: dónde buscar. `.` toma el `test.py` de la raíz;
  `tests` toma tus pruebas. Sin esto, `pytest` recorre todo el árbol
  (incluidos `__pycache__`, `.venv`, etc.).
- **`addopts`**: opciones que se aplican siempre. `-q` = salida corta.

Sin este archivo, `python -m pytest` no colecta el `test.py` de la
cátedra y te dice `no tests ran`. En la Iteración 3 el `pytest.ini` ya
tenía `python_files`; acá se le agrega `tests` a `testpaths`.

---

## 3. `conftest.py` — las fixtures compartidas

`pytest` **descubre** `tests/conftest.py` solo: no se importa desde
ningún lado. Todo lo que definas ahí queda disponible para cualquier
`test_*.py` de esa carpeta.

```python
# tests/conftest.py
@pytest.fixture
def titular():
    return PersonaFisica("Ana", "Perez", "12345678", 30)


@pytest.fixture
def banco():
    return Banco("Banco UTN")


@pytest.fixture
def banco_con_cuentas(banco, titular, empresa):
    banco.abrir_cuenta("AHORRO", titular, 1000)
    banco.abrir_cuenta("CORRIENTE", empresa, 1000, limite_descubierto=5000)
    return banco
```

Un test de `test_transferencias.py` declara el parámetro
`banco_con_cuentas` y lo recibe armado, sin importar nada. A su vez
`banco_con_cuentas` se apoya en `banco`, que se apoya en nada: es la
misma cadena de la Iteración 3, más larga.

Regla: **una fixture no arma más escenario del que el test necesita.**
Si `banco_con_cuentas` creciera a veinte cuentas, los tests se
vuelven lentos e ilegibles. Si un test necesita un caso raro, se lo
arma él.

### La fixture `autouse`

```python
@pytest.fixture(autouse=True)
def reiniciar_numeracion():
    Banco._ultimo_numero = 0
    yield
    Banco._ultimo_numero = 0
```

- `autouse=True`: se aplica a **todos** los tests sin que haya que
  pedirla por parámetro.
- El `yield` parte la fixture en dos: lo de arriba corre **antes** del
  test, lo de abajo **después**. Es el lugar para limpiar.
- Para qué: el contador de números de cuenta es un atributo de clase,
  vive entre tests. Sin reiniciarlo, los tests "pasan sueltos y
  fallan juntos" según el orden. Reiniciarlo antes **y** después deja
  a cada test aislado.

---

## 4. Herramientas nuevas de `pytest` en esta iteración

### 4.1 Capturar la excepción para inspeccionarla

```python
def test_los_errores_llevan_mensaje(ahorro):
    with pytest.raises(SaldoInsuficienteError) as info:
        ahorro.extraer(999_999)

    assert str(info.value).strip() != ""
```

`as info` te da un objeto con `.value` = la excepción que se lanzó.
Sirve para comprobar el mensaje, o el tipo exacto.

### 4.2 Jerarquía de excepciones: probar que un `except` viejo sigue andando

```python
def test_los_errores_de_validacion_siguen_siendo_value_error():
    assert issubclass(ErrorDeValidacion, ValueError)
    assert issubclass(MontoInvalidoError, ValueError)
```

La Iteración 4 introduce errores propios (`errores.py`). Estos tests
verifican que `MontoInvalidoError` **sigue siendo** un `ValueError`,
para que el código de las iteraciones 2 y 3 que hacía
`except ValueError` no se rompa. Es un test de **compatibilidad**.

### 4.3 El test de atomicidad: verificar que NO pasó nada

El patrón más importante de esta iteración. Una transferencia que
falla no debe dejar plata a medio mover:

```python
def test_una_transferencia_sin_fondos_no_deja_efectos_parciales(
        banco_con_cuentas):
    origen, destino = _cuentas(banco_con_cuentas)
    saldo_origen = origen.saldo
    saldo_destino = destino.saldo
    movimientos_destino = len(destino.historial())

    with pytest.raises(SaldoInsuficienteError):
        banco_con_cuentas.transferir(origen.cbu, destino.cbu, 999_999)

    assert origen.saldo == saldo_origen
    assert destino.saldo == saldo_destino
    assert len(destino.historial()) == movimientos_destino
```

Guardás el estado **antes**, provocás el fallo, y después comprobás
que **todo** quedó igual: los dos saldos y el historial del destino.
Cuando pruebes una operación que toca varios objetos, siempre
verificá el "no efecto" sobre todos.

### 4.4 El test de la hora argentina

```python
def test_movimiento_pone_su_propia_fecha_en_horario_argentino():
    movimiento = Movimiento("DEPOSITO", 100, 100)

    assert isinstance(movimiento.fecha_hora, datetime.datetime)
    assert movimiento.fecha_hora.utcoffset() == datetime.timedelta(hours=-3)
```

No se compara contra `datetime.now()` local (el runner de CI corre en
UTC): se comprueba que la fecha **trae zona** (`utcoffset()` no es
`None`) y que esa zona es UTC−3. El detalle de por qué está en
`TDD_ITERACION_04.md`, sección 8.

---

## 5. Cómo escribir tus tests en `tests/`

1. **Un archivo por tema.** El grupo ya tiene `test_banco.py`,
   `test_movimientos.py`, `test_transferencias.py`. Si agregás algo
   grande, `test_<tema>.py`.
2. **Importá del código, no de `test.py`.** `from cuentas import
   CuentaAhorro`.
3. **Usá las fixtures de `conftest.py`.** Si te falta una y la vas a
   usar en dos archivos, va al `conftest.py`. Si es de un solo
   archivo, definila arriba de ese archivo.
4. **Un test = un motivo para fallar.** Nombre en castellano que
   diga qué comprueba.
5. **Preparar / Actuar / Verificar**, separados por línea en blanco.

### Cuándo agregar un test (además de los que ya están)

- **Encontraste un bug:** antes de arreglarlo, escribí el test que lo
  reproduce y falla. Arreglás. El test pasa. Queda de por vida como
  test de **regresión** (que no vuelva).
- **Un caso límite que el contrato no cubre:** transferir exactamente
  todo el saldo, cerrar una cuenta con saldo cero justo, un CBU con
  el último dígito en 0.
- **Una regla de negocio del grupo** que no está en `test.py`.

### Ejemplo completo

```python
# tests/test_cuentas.py
import pytest
from cuentas import CuentaAhorro
from errores import SaldoInsuficienteError


def test_extraer_exactamente_el_saldo_deja_la_cuenta_en_cero(titular):
    cuenta = CuentaAhorro("00000000000017", titular, 1000)

    cuenta.extraer(1000)

    assert cuenta.saldo == 0


def test_extraer_un_centavo_de_mas_no_toca_el_saldo(titular):
    cuenta = CuentaAhorro("00000000000017", titular, 1000)

    with pytest.raises(SaldoInsuficienteError):
        cuenta.extraer(1000.01)

    assert cuenta.saldo == 1000
```

---

## 6. Checklist

- [ ] `python -m pytest -q` termina en `passed`, sin `error` ni
      `failed`, antes de entregar.
- [ ] Tus tests están en `tests/`, no en `test.py`.
- [ ] No modificaste `test.py` ni `pytest.ini`.
- [ ] Cada test nuevo tiene nombre descriptivo en castellano y los
      tres bloques.
- [ ] Los casos "tiene que fallar" verifican además que el estado no
      cambió.
- [ ] Si arreglaste un bug, dejaste el test de regresión.
- [ ] Las fixtures compartidas están en `conftest.py`; ninguna arma
      más de lo necesario.
