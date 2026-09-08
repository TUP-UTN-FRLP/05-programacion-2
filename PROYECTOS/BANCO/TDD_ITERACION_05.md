# Contrato de comportamiento y guía de pruebas — Iteración 5

> Última iteración. La suite deja de ser "los tests del ejercicio" y toma la
> forma de una suite de proyecto: organizada por módulo, con fixtures
> compartidas, **tests parametrizados sobre toda la jerarquía**, dobles de
> prueba, umbral de cobertura y verificación automática en cada Pull Request.
>
> La novedad conceptual: hasta ahora los tests verificaban **comportamiento**.
> Ahora también verifican **diseño**.

## Índice

1. Organización de la suite
2. `conftest.py` y fixtures parametrizadas
3. Tests de contrato de subclase (LSP)
4. Tests de extensibilidad (OCP)
5. Contrato de las clases abstractas
6. Contrato de `Movimiento` como `dataclass`
7. Contrato de `RepositorioCuentas`
8. Dobles de prueba: para qué sirvió el DIP
9. Contrato de `Banco` con repositorio inyectado
10. Cobertura y umbral
11. Integración continua
12. Definición de terminado
13. Trazabilidad requisito → prueba

---

## 1. Organización de la suite

```text
tests/
    __init__.py
    conftest.py
    test_personas.py
    test_cuentas.py
    test_movimientos.py
    test_banco.py
    test_repositorios.py
    test_principios.py     # LSP, OCP, abstracción
test.py                    # contrato de la cátedra, sin modificar
```

Un archivo de test por módulo de producción, con el mismo nombre. Cuando algo
falla, el nombre del archivo dice dónde mirar.

`pytest.ini`:

```ini
[pytest]
python_files = test.py test_*.py
testpaths = . tests
markers =
    principios: verifica una propiedad de diseño, no un comportamiento
addopts = -q --strict-markers
```

`--strict-markers` hace fallar la suite si se usa un marcador no declarado: sin
esa opción, un `@pytest.mark.principos` mal escrito se acepta en silencio y el
filtro nunca lo encuentra.

```bash
python -m pytest -m principios       # solo los tests de diseño
python -m pytest -m "not principios" # solo comportamiento
```

---

## 2. `conftest.py` y fixtures parametrizadas

```python
import pytest

from banco import (Banco, CuentaAhorro, CuentaCorriente, CuentaSueldo,
                   PersonaFisica, PersonaJuridica, RepositorioMemoria)

CLASES_CONCRETAS = (CuentaAhorro, CuentaCorriente, CuentaSueldo)


@pytest.fixture
def titular():
    return PersonaFisica("Ana", "Perez", "12345678", 30)


@pytest.fixture
def empresa():
    return PersonaJuridica("Distribuidora S.A.", "30712345671")


@pytest.fixture
def banco():
    return Banco("Banco UTN", RepositorioMemoria())


@pytest.fixture(params=CLASES_CONCRETAS, ids=lambda c: c.__name__)
def cualquier_cuenta(request, titular):
    """Una instancia de CADA tipo concreto de cuenta, con $10.000."""
    clase = request.param
    return clase("00000123456789", titular, 10_000)
```

La última es la fixture clave de la iteración. Un test que la reciba **se
ejecuta una vez por cada tipo de cuenta**, y la salida los identifica por
nombre:

```text
tests/test_cuentas.py::test_deposito_aumenta_el_saldo[CuentaAhorro]  PASSED
tests/test_cuentas.py::test_deposito_aumenta_el_saldo[CuentaCorriente] PASSED
tests/test_cuentas.py::test_deposito_aumenta_el_saldo[CuentaSueldo]  PASSED
```

Cuando en el futuro se agregue un cuarto tipo, alcanza con sumarlo a
`CLASES_CONCRETAS`: toda la batería de contrato se le aplica sola. Eso es una
suite que acompaña el diseño en lugar de frenarlo.

---

## 3. Tests de contrato de subclase (LSP)

Todo lo que valga para `Cuenta` debe valer para cualquier subclase. Se escribe
una vez y se ejecuta para todas.

```python
def test_deposito_aumenta_el_saldo(cualquier_cuenta):
    saldo_previo = cualquier_cuenta.saldo

    cualquier_cuenta.depositar(500)

    assert cualquier_cuenta.saldo == saldo_previo + 500


def test_deposito_registra_un_movimiento(cualquier_cuenta):
    previos = len(cualquier_cuenta.historial())

    cualquier_cuenta.depositar(500)

    assert len(cualquier_cuenta.historial()) == previos + 1


@pytest.mark.parametrize("monto_invalido", [0, -1, -0.01])
def test_deposito_invalido_es_rechazado(cualquier_cuenta, monto_invalido):
    saldo_previo = cualquier_cuenta.saldo

    with pytest.raises(MontoInvalidoError):
        cualquier_cuenta.depositar(monto_invalido)

    assert cualquier_cuenta.saldo == saldo_previo


def test_saldo_es_de_solo_lectura(cualquier_cuenta):
    with pytest.raises(AttributeError):
        cualquier_cuenta.saldo = 999_999


def test_cierre_de_periodo_responde_en_todas(cualquier_cuenta):
    cualquier_cuenta.cierre_de_periodo()      # ninguna debe romper


def test_cuenta_cerrada_no_opera(cualquier_cuenta):
    cualquier_cuenta.extraer(cualquier_cuenta.saldo)
    cualquier_cuenta.cerrar()

    with pytest.raises(CuentaInactivaError):
        cualquier_cuenta.depositar(100)
```

Contrato completo que debe cumplir **toda** subclase concreta:

| # | Regla | Cómo se verifica |
| --- | --- | --- |
| L1 | hereda de `Cuenta` | `issubclass` |
| L2 | se puede instanciar con `(numero, titular, saldo_inicial)` | la fixture |
| L3 | no sobrescribe `extraer` ni `depositar` | `"extraer" not in clase.__dict__` |
| L4 | redefine `TIPO` | `clase.TIPO != Cuenta.TIPO` |
| L5 | implementa `_validar_extraccion` y `cierre_de_periodo` | `clase.__abstractmethods__ == frozenset()` |
| L6 | no relaja las validaciones de la base | los tests de monto inválido pasan para todas |
| L7 | `historial()` devuelve una copia | `clear()` sobre el resultado no afecta |
| L8 | extracción rechazada no modifica el saldo | test por tipo con su propio límite |

Los puntos L1 a L5 van en `test_principios.py`, parametrizados sobre
`CLASES_CONCRETAS`:

```python
@pytest.mark.principios
@pytest.mark.parametrize("clase", CLASES_CONCRETAS, ids=lambda c: c.__name__)
def test_ninguna_subclase_duplica_el_algoritmo_base(clase):
    assert "extraer" not in clase.__dict__
    assert "depositar" not in clase.__dict__
```

---

## 4. Tests de extensibilidad (OCP)

```python
@pytest.mark.principios
def test_el_banco_conoce_los_tres_tipos():
    assert set(Banco.TIPOS_DE_CUENTA) == {"AHORRO", "CORRIENTE", "SUELDO"}


@pytest.mark.principios
def test_todos_los_tipos_registrados_son_cuentas():
    for clase in Banco.TIPOS_DE_CUENTA.values():
        assert issubclass(clase, Cuenta)
        assert not inspect.isabstract(clase)


@pytest.mark.principios
def test_abrir_cuenta_funciona_para_todos_los_tipos(banco, titular):
    for tipo in Banco.TIPOS_DE_CUENTA:
        cuenta = banco.abrir_cuenta(tipo, titular)
        assert cuenta.cbu in banco
```

El último test es el más valioso: recorre el diccionario en vez de nombrar los
tipos uno por uno, así que **cubre automáticamente cualquier tipo que se agregue
en el futuro**. Un test que hay que editar cada vez que se extiende el sistema
es un test que viola el mismo principio que pretende verificar.

### El diff como evidencia

Además de los tests, la entrega incluye en el README:

```bash
git diff <hash-previo-a-cuenta-sueldo> --stat
```

Debe mostrar archivos nuevos (`cuentas.py` con la clase agregada, tests nuevos)
y **una línea** modificada en `banco.py`. Si toca `Cuenta`, `CuentaAhorro` o
`CuentaCorriente`, el principio no se cumplió: documentar por qué.

---

## 5. Contrato de las clases abstractas

| Caso | Esperado |
| --- | --- |
| `Persona("Ana")` | `TypeError` |
| `Cuenta("00000123456789", titular)` | `TypeError` |
| `RepositorioCuentas()` | `TypeError` |
| `Cuenta.__abstractmethods__` | contiene `tipo`, `_validar_extraccion`, `cierre_de_periodo` |
| `CuentaAhorro.__abstractmethods__` | `frozenset()` (vacío) |
| una subclase de prueba que no implemente todo | no se puede instanciar |

Test de la última fila:

```python
@pytest.mark.principios
def test_una_subclase_incompleta_no_se_instancia(titular):
    class CuentaIncompleta(Cuenta):
        pass

    with pytest.raises(TypeError):
        CuentaIncompleta("00000123456789", titular)
```

Definir una clase dentro de un test es legítimo cuando la clase existe solo para
la verificación: no ensucia el código de producción.

---

## 6. Contrato de `Movimiento` como `dataclass`

| Caso | Esperado |
| --- | --- |
| `Movimiento("DEPOSITO", 100, 1100)` | se construye; `fecha_hora` cercana a la hora argentina |
| `movimiento.fecha_hora.tzinfo` | no es `None` |
| `movimiento.fecha_hora.utcoffset()` | `timedelta(hours=-3)` |
| dos movimientos creados con microsegundos de diferencia | `fecha_hora` **distintas** |
| `movimiento.monto = 999` | `dataclasses.FrozenInstanceError` |
| `movimiento.fecha_hora = otra` | `FrozenInstanceError` |
| `Movimiento("RETIRO", 100, 0)` | error de validación (`__post_init__`) |
| `Movimiento("DEPOSITO", 0, 0)` | `MontoInvalidoError` |
| `Movimiento("DEPOSITO", True, 0)` | `ErrorDeTipo` |
| dos movimientos con los mismos valores y la misma fecha | son `==` (lo da el `dataclass`) |
| `repr(movimiento)` | contiene los cuatro campos |
| `str(movimiento)` | formato legible, escrito a mano |
| `"RETENCION" in Movimiento.TIPOS` | `True` |

El test de las fechas distintas es el que atrapa el error de usar `default` en
lugar de `default_factory`:

```python
def test_cada_movimiento_tiene_su_propia_fecha():
    primero = Movimiento("DEPOSITO", 100, 100)
    segundo = Movimiento("DEPOSITO", 100, 200)

    assert primero.fecha_hora != segundo.fecha_hora
```

La `default_factory` no es `datetime.now` a secas: es una función chica que
devuelve `datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))`. Se envuelve
en una función porque `field(default_factory=...)` espera un invocable sin
argumentos, y porque así el `dataclass` queda con la hora argentina (UTC−3) sin
depender de la zona en la que corra el proceso.

```python
def test_la_fecha_esta_en_zona_argentina():
    m = Movimiento("DEPOSITO", 100, 100)

    assert m.fecha_hora.tzinfo is not None
    assert m.fecha_hora.utcoffset() == timedelta(hours=-3)
```

---

## 7. Contrato de `RepositorioCuentas`

Lo que debe cumplir **cualquier** implementación, hoy `RepositorioMemoria` y
mañana el de Django. Se escribe parametrizado sobre las implementaciones
disponibles:

```python
IMPLEMENTACIONES = (RepositorioMemoria,)


@pytest.fixture(params=IMPLEMENTACIONES, ids=lambda c: c.__name__)
def repositorio(request):
    return request.param()
```

| Caso | Esperado |
| --- | --- |
| repositorio recién creado | `cantidad() == 0`, `listar() == []` |
| `agregar(cuenta)` | `existe(cuenta.cbu)` es `True` |
| `obtener(cbu)` | devuelve **el mismo objeto** (`is`) |
| `obtener(cbu)` inexistente | `CuentaInexistenteError` |
| `agregar()` con un CBU ya presente | `CuentaDuplicadaError` |
| `agregar()` algo que no es una `Cuenta` | `ErrorDeTipo` |
| `listar()` | lista nueva; `.clear()` no afecta al repositorio |
| `cantidad()` | coincide con `len(listar())` |
| `existe()` con un CBU inexistente | `False`, sin lanzar excepción |

Cuando aparezca una segunda implementación, se la suma a `IMPLEMENTACIONES` y la
batería completa se le aplica sin escribir un test más. Eso es un **test de
contrato**: verifica la abstracción, no la implementación.

---

## 8. Dobles de prueba: para qué sirvió el DIP

Con el repositorio inyectado se pueden pasar implementaciones falsas que serían
imposibles de construir con un `dict` adentro del `Banco`.

### Un repositorio que cuenta llamadas

```python
class RepositorioEspia(RepositorioMemoria):
    def __init__(self):
        super().__init__()
        self.llamadas_a_obtener = 0

    def obtener(self, cbu):
        self.llamadas_a_obtener += 1
        return super().obtener(cbu)


def test_transferir_busca_las_dos_cuentas_una_sola_vez(titular):
    espia = RepositorioEspia()
    banco = Banco("Banco UTN", espia)
    origen = banco.abrir_cuenta("AHORRO", titular, 1000)
    destino = banco.abrir_cuenta("AHORRO", titular, 0)
    espia.llamadas_a_obtener = 0

    banco.transferir(origen.cbu, destino.cbu, 500)

    assert espia.llamadas_a_obtener == 2
```

### Un repositorio que falla

```python
class RepositorioQueFalla(RepositorioMemoria):
    def agregar(self, cuenta):
        raise ErrorDeRegistro("almacenamiento no disponible")


def test_el_banco_propaga_el_error_del_repositorio(titular):
    banco = Banco("Banco UTN", RepositorioQueFalla())

    with pytest.raises(ErrorDeRegistro):
        banco.abrir_cuenta("AHORRO", titular)
```

Simular un fallo de almacenamiento sin tener almacenamiento real es exactamente
lo que el DIP compra. Vale la pena señalarlo en la defensa: el principio no es
una formalidad, se paga solo en la suite.

---

## 9. Contrato de `Banco` con repositorio inyectado

| Caso | Esperado |
| --- | --- |
| `Banco("Banco UTN")` sin repositorio | usa un `RepositorioMemoria` por defecto |
| `Banco("Banco UTN", RepositorioMemoria())` | usa el que se le pasó |
| `Banco("Banco UTN", {})` | `ErrorDeTipo` |
| `Banco("Banco UTN", "memoria")` | `ErrorDeTipo` |
| dos bancos con repositorios distintos | no comparten cuentas |
| `banco.__dict__` | **no** contiene ningún `dict`, `list` ni `set` de cuentas |
| `cierre_de_mes()` | invoca `cierre_de_periodo()` en todas las cuentas activas |
| `cierre_de_mes()` | no contiene ningún `isinstance` ni comparación de `TIPO` |

Los últimos tres son tests de diseño:

```python
@pytest.mark.principios
def test_el_banco_no_guarda_cuentas_directamente(banco):
    for valor in vars(banco).values():
        assert not isinstance(valor, (dict, list, set)), (
            "Banco guarda una colección de cuentas: debe delegar en el repositorio"
        )


@pytest.mark.principios
def test_el_cierre_de_mes_no_pregunta_tipos():
    codigo = inspect.getsource(Banco.cierre_de_mes)
    assert "isinstance" not in codigo
    assert "TIPO" not in codigo
```

El segundo lee el código fuente del método con `inspect.getsource`. Es una
verificación rudimentaria y se la puede engañar; no está para atrapar a nadie,
sino para que un `isinstance` agregado a las tres de la mañana aparezca en el
Pull Request y no seis meses después.

---

## 10. Cobertura y umbral

```bash
python -m pip install pytest-cov
python -m pytest --cov=banco --cov-report=term-missing --cov-fail-under=85
```

| Módulo | Mínimo |
| --- | --- |
| `banco/cuentas.py`, `banco/personas.py`, `banco/movimientos.py` | 90 % |
| `banco/banco.py`, `banco/repositorios.py` | 90 % |
| `banco/validaciones.py`, `banco/errores.py` | 85 % |
| `main.py` | sin exigencia |
| total del paquete | 85 % |

`--cov-fail-under` hace que la suite falle si no se llega: es la diferencia
entre "medimos la cobertura" y "la cobertura es un requisito".

Recordatorio de la Iteración 4: la cobertura mide qué líneas se ejecutaron, no
qué se verificó. Sirve para encontrar ramas de error nunca probadas —donde
suelen esconderse los errores—, no como calificación.

Reporte navegable:

```bash
python -m pytest --cov=banco --cov-report=html    # htmlcov/index.html
```

`htmlcov/` y `.coverage` van al `.gitignore`.

---

## 11. Integración continua (recomendado)

`.github/workflows/ci.yml`:

```yaml
name: tests

on:
  push:
  pull_request:

jobs:
  pytest:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      - run: python -m pip install -r requirements.txt
      - run: python -m pytest --cov=banco --cov-fail-under=85
```

Con esto, cada Pull Request individual muestra si la suite pasa **antes** de que
el líder lo revise. Deja de existir la discusión "en mi máquina anda": la
máquina es la misma para todos.

Es opcional para la nota, pero conviene configurarlo en la primera integración
de la semana: son quince minutos y ahorra la mayor parte de los conflictos.

---

## 12. Definición de terminado

Una iteración está terminada cuando **todo** esto es cierto:

- [ ] `python -m pytest -q` pasa, sin tests salteados;
- [ ] `test.py` de la cátedra pasa sin haber sido modificado;
- [ ] los tests marcados `principios` pasan;
- [ ] la cobertura llega al umbral;
- [ ] los `assert` de `main.py` no fallan al arrancar;
- [ ] el `git diff --stat` de `CuentaSueldo` está en el README;
- [ ] `git status` está limpio y `.gitignore` cubre lo generado;
- [ ] no hay código comentado ni `print()` de depuración fuera de `main.py`;
- [ ] el README permite a alguien externo ejecutar el sistema;
- [ ] cada integrante puede explicar cualquier archivo del proyecto.

El último punto no es retórico: es el criterio con el que se evalúa.

---

## 13. Trazabilidad requisito → prueba

Se completa esta tabla en el README del grupo. Sirve para detectar requisitos
sin cobertura y para la defensa oral.

| # | Requisito | Iter. | Prueba que lo verifica |
| --- | --- | --- | --- |
| R1 | El saldo no se modifica desde afuera | 2 | `test_cuentas.py::test_saldo_es_de_solo_lectura` |
| R2 | El CUIT tiene dígito verificador válido | 3 | `test_personas.py::test_cuit_invalido_es_rechazado` |
| R3 | Una caja de ahorro nunca queda en negativo | 3 | `test_cuentas.py::test_ahorro_sin_descubierto` |
| R4 | La cuenta corriente respeta su límite | 3 | `test_cuentas.py::test_limite_de_descubierto` |
| R5 | Toda operación deja un movimiento | 4 | `test_cuentas.py::test_deposito_registra_un_movimiento` |
| R6 | Una transferencia fallida no deja efectos | 4 | `test_banco.py::test_transferencia_fallida_no_acredita` |
| R7 | Cerrar una cuenta no borra su historial | 4 | `test_banco.py::test_baja_logica_conserva_historial` |
| R8 | Todo error del sistema es un `BancoError` | 4 | `test_banco.py::test_jerarquia_de_errores` |
| R9 | Las clases base no se instancian | 5 | `test_principios.py::test_clases_abstractas` |
| R10 | Un tipo nuevo no obliga a tocar los existentes | 5 | `test_principios.py::test_abrir_cuenta_funciona_para_todos_los_tipos` |
| R11 | Un movimiento no se modifica | 5 | `test_movimientos.py::test_movimiento_es_inmutable` |
| R12 | `Banco` no depende de una estructura concreta | 5 | `test_principios.py::test_el_banco_no_guarda_cuentas_directamente` |

Un requisito sin prueba es una intención. Una prueba sin requisito suele ser una
prueba de la implementación y no del comportamiento: conviene revisarla.
