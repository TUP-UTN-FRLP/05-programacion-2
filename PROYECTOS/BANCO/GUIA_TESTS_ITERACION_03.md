# Guía para desarrollar los tests — Iteración 3

> **Desde esta iteración `pytest` se ejecuta.** El `test.py` de la
> cátedra deja de ser un documento de lectura: se corre, y **que pase
> es condición de entrega**. Además, cada estudiante escribe sus
> propios tests, tomando como molde el `test.py` de la **Iteración 2**
> (`ITERACION-02/test.py`), que ya conocés línea por línea.

Documento hermano: `TDD_ITERACION_03.md` (el contrato: qué nombres y
qué comportamiento se exigen). Acá se explica la **herramienta** y
**cómo escribir los tuyos**.

---

## 1. De qué se trata testear

Hasta la Iteración 2 verificabas el código "a ojo": corrías
`banco.py`, mirabas la salida y decidías si estaba bien. Eso no
escala. Un test es lo mismo, pero **escrito una vez y repetible**: una
función chica que prepara un objeto, ejecuta una operación y comprueba
el resultado con `assert`.

```python
def test_el_deposito_aumenta_el_saldo():
    cuenta = CuentaAhorro("00000123456789", titular)
    cuenta.depositar(1000)

    cuenta.depositar(500)

    assert cuenta.saldo == 1500
```

Fijate que la cuenta se crea sin saldo (nace en `0`) y el `$1000` se carga
con un `depositar()`, igual que el `$500` posterior: ninguna cuenta se abre
con fondos ya cargados (ver el porqué en la sección 2.5).

Si `saldo` no vale `1500`, el `assert` corta y el test "falla". Si
vale, no pasa nada y el test "pasa". Nada más.

`assert` a secas es la forma artesanal. `pytest` le agrega arriba unas
pocas comodidades que `test.py` usa todo el tiempo (sección 3).

---

## 2. Puesta en marcha

### 2.1 Instalar y correr

```bash
python -m pip install pytest
python -m pytest -q
```

Siempre con `python -m pytest`, **no** `pytest` a secas: el `-m` mete
la carpeta actual en el `sys.path`, y sin eso los `from banco import
...` de la suite no resuelven.

Salida esperada: una línea de puntos y `NNN passed`. Si algo falla,
`pytest` te muestra el archivo, la línea, el `assert` que cortó y los
valores reales:

```text
FAILED test.py::test_el_deposito_aumenta_el_saldo - assert 1200 == 1500
```

Comandos que vas a usar:

| Comando | Para qué |
| --- | --- |
| `python -m pytest -q` | toda la suite, salida corta |
| `python -m pytest test.py` | solo el contrato de la cátedra |
| `python -m pytest -k cuit` | los tests cuyo nombre contiene "cuit" |
| `python -m pytest -x` | frená en el primer fallo |
| `python -m pytest --lf` | corré solo los que fallaron la vez pasada |
| `python -m pytest -q -v` | mostrá el nombre de cada caso |

### 2.2 `pytest.ini` — por qué hace falta

Va en la raíz de la carpeta de la iteración, al lado de `banco.py`:

```ini
[pytest]
python_files = test.py test_*.py
testpaths = .
addopts = -q
```

- **`python_files`**: qué archivos son suites. Por defecto `pytest`
  toma solo `test_*.py` y `*_test.py`. El archivo de la cátedra se
  llama `test.py` a secas, así que hay que nombrarlo explícitamente.
  Tus archivos propios sí siguen la convención `test_*.py`.
- **`testpaths`**: dónde buscar. `.` = la carpeta de la iteración. Sin
  esto, `pytest` recorre todo el árbol (`__pycache__`, `.venv`, etc.).
- **`addopts`**: opciones que se aplican siempre. `-q` = salida corta.

Sin este archivo, `python -m pytest` te dice `no tests ran`.

### 2.3 `.gitignore`

Al empezar a correr `pytest` aparecen dos carpetas que **no se
versionan**. Agregá al `.gitignore`:

```text
__pycache__/
.pytest_cache/
```

### 2.4 Qué se toca y qué no

```text
banco.py           # tu código
validaciones.py    # tu código
test.py            # contrato de la cátedra: SE EJECUTA, NO SE MODIFICA
test_propios.py    # TUS pruebas (el nombre es libre, con prefijo test_)
pytest.ini
.gitignore
```

`test.py` no se edita nunca: si algo no pasa, se arregla `banco.py` o
`validaciones.py`, no el test.

### 2.5 Regla nueva: ninguna cuenta se crea con saldo

> **Importante para escribir tus tests:** desde esta iteración
> `Cuenta`, `CuentaAhorro` y `CuentaCorriente` **no reciben
> `saldo_inicial` en el constructor**. Toda cuenta nace con `saldo ==
> 0`. El banco no permite abrir una cuenta con fondos ya cargados: si
> hay que darle un saldo inicial, se hace con una llamada a
> `depositar()` después de crearla, como cualquier otro movimiento. Si
> tu fixture de `ahorro` o `corriente` todavía crea la cuenta pasando
> un tercer argumento numérico, está usando el diseño viejo: armala
> con `depositar()` (ver el ejemplo en 3.2).

---

## 3. Las herramientas de `pytest` que aparecen en `test.py`

### 3.1 `assert` con el mensaje que arma pytest

Con `pytest` no necesitás escribir el mensaje de error: si

```python
assert cuenta.saldo == 1500
```

falla, la salida te muestra sola `assert 1200 == 1500`. Por eso los
tests no llevan `assert x == y, "saldo mal"`: sobra.

### 3.2 Fixtures — el escenario que se repite

Casi todos los tests arrancan con "una persona física", "una caja de
ahorro con $1000". En la Iteración 2, `test.py` resolvía eso con una
**función común**:

```python
def crear_titular():
    return Persona("Ana", "Pérez", "12345678")


def test_depositar_aumenta_el_saldo():
    cuenta = Cuenta(NUMERO_VALIDO, crear_titular(), 100)
    ...
```

Funciona, pero hay que acordarse de llamarla en cada test. La versión
`pytest` es una **fixture**: se define **una vez** con
`@pytest.fixture` y el test la **pide por nombre**, como si fuera un
parámetro.

```python
@pytest.fixture
def fisica():
    return PersonaFisica("ana maría", "pérez", "12345678", 30)


@pytest.fixture
def ahorro(fisica):
    cuenta = CuentaAhorro(NUMERO, fisica)
    cuenta.depositar(1000)
    return cuenta


def test_el_deposito_aumenta_el_saldo(ahorro):
    ahorro.depositar(500)
    assert ahorro.saldo == 1500
```

`pytest` ve el parámetro `ahorro`, ejecuta la función `ahorro()`, te
pasa el resultado y **crea uno nuevo para cada test**: si un test rompe
la cuenta, el siguiente arranca con una intacta. Fijate que `ahorro` a
su vez pide `fisica`: las fixtures se encadenan, igual que
`crear_titular()` se llamaba desde otras funciones.

En `test.py` las fixtures son `fisica`, `juridica`, `ahorro`,
`corriente`.

### 3.3 `pytest.raises` — cuando lo correcto es que explote

La mitad del contrato dice "esto tiene que fallar": un CUIT con dígito
verificador mal, extraer más de lo que hay, un nombre con números. No
podés escribir `assert` sobre una excepción; usás un `with`:

```python
def test_la_cuenta_ahorro_no_permite_saldo_negativo(ahorro):
    with pytest.raises(ValueError):
        ahorro.extraer(1000.01)

    assert ahorro.saldo == 1000
```

Lee así: "dentro de este bloque **espero** un `ValueError`; si no se
lanza, el test falla; si se lanza otra cosa, también". El `assert` de
abajo, fuera del `with`, comprueba el efecto colateral: que la
extracción rechazada **no tocó el saldo**.

`TypeError` y `ValueError` no son lo mismo y el contrato los distingue:
`TypeError` = "me pasaste algo del tipo equivocado"
(`validar_cuit(30712345671)` con un `int`); `ValueError` = "el tipo
está bien pero el valor no sirve" (`validar_cuit("30712345670")`).

### 3.4 `pytest.mark.parametrize` — el mismo test con muchos datos

Cuando el caso es idéntico y solo cambia el dato de entrada, no se
copia el test: se lista arriba con un decorador. Esto ya lo veías en la
Iteración 2:

```python
@pytest.mark.parametrize("invalido", [
    "30712345670",     # verificador incorrecto
    "3071234567",      # 10 dígitos
    "307123456712",    # 12 dígitos
    "30-71234567-1",   # con guiones
    "3071234567a",     # con letras
    "",
    "   ",
])
def test_validar_cuit_rechaza_valores_invalidos(invalido):
    with pytest.raises(ValueError):
        validar_cuit(invalido)
```

Eso es **un** test escrito, pero **siete** casos ejecutados: `pytest`
corre el cuerpo una vez por cada elemento de la lista. En la salida
aparecen como
`test_validar_cuit_rechaza_valores_invalidos[3071234567]`, etc.

Se puede parametrizar con dos variables:

```python
@pytest.mark.parametrize("atributo, valor", [
    ("nombre", "Otro"),
    ("apellido", "Otro"),
    ("dni", "99999999"),
    ("edad", 99),
])
def test_los_datos_de_persona_fisica_son_de_solo_lectura(
        fisica, atributo, valor):
    with pytest.raises(AttributeError):
        setattr(fisica, atributo, valor)
```

### 3.5 `pytest.approx` — comparar `float` sin llorar

`1000 * 0.01` no siempre da exactamente `10.0` en punto flotante. Para
esas comparaciones:

```python
assert interes == pytest.approx(10)
assert cuenta.saldo == pytest.approx(1010)
```

---

## 4. La anatomía de todo test: Preparar / Actuar / Verificar

Mirá cualquier función de `test.py` y vas a ver tres bloques separados
por una línea en blanco:

```python
def test_liquidar_interes_acredita_y_devuelve_el_interes(fisica):
    cuenta = CuentaAhorro(NUMERO, fisica, 0.01)          # Preparar
    cuenta.depositar(1000)                               # Preparar

    interes = cuenta.liquidar_interes()                  # Actuar

    assert interes == pytest.approx(10)                 # Verificar
    assert cuenta.saldo == pytest.approx(1010)
```

- **Preparar:** armás el objeto en el estado que te interesa.
- **Actuar:** ejecutás **una** operación. Una sola.
- **Verificar:** uno o más `assert` sobre el resultado y sobre el
  estado que quedó.

Un test que "actúa" tres veces no te dice cuál de las tres rompió.

---

## 5. Cómo armar tus propios tests tomando como base `ITERACION-02/test.py`

El `test.py` de la Iteración 2 es tu plantilla. Ya lo leíste entero; ahora
lo usás como referencia de forma.

### 5.1 Copiá el esqueleto

Todo archivo de tests tiene la misma estructura que
`ITERACION-02/test.py`:

```python
"""Pruebas propias — Iteración 3.

Qué cubre: <en una frase>.
"""

import pytest

from banco import CuentaAhorro, CuentaCorriente, PersonaFisica, PersonaJuridica
from validaciones import validar_cuit, validar_edad

NUMERO = "00000123456789"          # 14 dígitos, con nombre para no repetirlo


# --------------------------------------------------------------------- #
# validar_cuit
# --------------------------------------------------------------------- #

def test_...():
    ...
```

Los separadores con `# ---` no son decoración: agrupan los tests por lo
que prueban, igual que en el archivo de la cátedra.

### 5.2 De `crear_titular()` a fixture

En la Iteración 2 tenías:

```python
def crear_titular():
    return Persona("Ana", "Pérez", "12345678")
```

En la 3, `Persona` genérica ya no representa a un titular real: el
titular es una `PersonaFisica` o una `PersonaJuridica`. Convertilo en
fixture:

```python
@pytest.fixture
def titular():
    return PersonaFisica("Ana", "Perez", "12345678", 30)
```

y donde antes escribías `crear_titular()` ahora ponés `titular` como
parámetro del test.

### 5.3 Cada caso de la Iteración 2 tiene su equivalente en la 3

Escribís los tuyos calcando el molde del caso análogo:

| Molde en `ITERACION-02/test.py` | Tu test de la Iteración 3 |
| --- | --- |
| `test_validar_dni_acepta_7_u_8_digitos` (parametrizado, happy path) | `test_validar_cuit_acepta_cuit_con_verificador_valido` |
| `test_validar_dni_rechaza_formato_invalido` (parametrize + `raises(ValueError)`) | `test_validar_edad_rechaza_menores_de_18` |
| `test_validar_dni_rechaza_tipo_incorrecto` (`raises(TypeError)`) | `test_validar_edad_rechaza_float_y_bool` |
| `test_propiedades_de_persona_son_solo_lectura` (`raises(AttributeError)`) | `test_la_tasa_de_interes_es_de_solo_lectura` |
| `test_extraer_rechaza_saldo_insuficiente_sin_cambiar_saldo` (raises + assert de estado) | `test_la_caja_de_ahorro_no_permite_descubierto` |
| `test_depositar_aumenta_el_saldo` (Preparar/Actuar/Verificar) | `test_liquidar_interes_acredita_el_saldo` |

### 5.4 Qué agregar además de lo que ya está en `test.py`

- **Un caso límite que el contrato no cubre:** extraer exactamente
  hasta el límite del descubierto (`saldo - monto == -limite`),
  liquidar interés sobre saldo `0`, un CUIT válido con prefijo `27`.
- **Un bug que encontraste:** antes de arreglarlo, escribí el test que
  lo reproduce y falla. Arreglás. El test pasa. Queda de por vida como
  test de **regresión**.
- **Una regla que decidió tu grupo** y no está en `test.py`.

No repitas los casos que ya están en el `test.py` de la cátedra: esos
ya se ejecutan.

### 5.5 Reglas de forma (las mismas del archivo de la cátedra)

- El nombre empieza con `test_` y dice qué comprueba, en castellano,
  sin abreviar: `test_la_extraccion_rechazada_no_modifica_el_saldo`.
- Tres bloques Preparar / Actuar / Verificar separados por línea en
  blanco.
- "Actúa" una sola vez.
- Si el caso es "tiene que fallar": `with pytest.raises(...)` **y**
  además un `assert` de que el estado no cambió.
- Mismo cuerpo con distintos datos → `@pytest.mark.parametrize`, no
  tres funciones.
- Escenario repetido → fixture, no copiado.
- `float` → `pytest.approx`.

---

## 6. Dos cosas nuevas respecto de la Iteración 2

### Invariantes

No todos los tests miran un caso: algunos miran una propiedad que
**siempre** tiene que valer.

```python
@pytest.mark.parametrize("clase", [CuentaAhorro, CuentaCorriente])
def test_ninguna_subclase_redefine_depositar(clase):
    assert "depositar" not in clase.__dict__
```

Esto no prueba un depósito: prueba que `depositar` **no está escrito**
en la subclase, o sea que no duplicaste código. `clase.__dict__` son
los atributos definidos en esa clase (no los heredados).

### Contrato de subclase

```python
@pytest.mark.parametrize("clase", [CuentaAhorro, CuentaCorriente])
def test_toda_subclase_redefine_el_tipo(clase):
    assert clase.TIPO != Cuenta.TIPO
```

Cualquier tipo de cuenta que agregues en el futuro se suma a esa lista
y tiene que cumplir lo mismo. Es la idea que se formaliza en la
Iteración 5.

---

## 7. Cuando pases a la Iteración 4

Lo que ya sabés (correr `pytest`, fixtures, `raises`, `parametrize`,
`pytest.ini`) se conserva. Se suma la organización en varios archivos:
una carpeta `tests/` con un `conftest.py` para las fixtures
compartidas, y `pytest.ini` pasa a incluir `tests` en `testpaths`. Lo
explica `GUIA_TESTS_ITERACION_04.md`.

---

## 8. Checklist

- [ ] `python -m pytest -q` termina en `passed`, sin `error` ni
      `failed`, antes de entregar.
- [ ] `pytest.ini` está en la raíz, con `python_files = test.py
      test_*.py`.
- [ ] `.pytest_cache/` y `__pycache__/` están en `.gitignore`.
- [ ] No modificaste `test.py`.
- [ ] Tus tests están en un archivo `test_*.py` aparte.
- [ ] Cada test nuevo tiene nombre descriptivo en castellano y los tres
      bloques Preparar / Actuar / Verificar.
- [ ] Los casos "tiene que fallar" verifican además que el estado no
      cambió.
- [ ] El escenario repetido está en una fixture; los `float` se
      comparan con `pytest.approx`.
- [ ] Si arreglaste un bug, dejaste el test de regresión.
