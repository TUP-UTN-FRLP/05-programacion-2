# Guía para desarrollar los tests — Iteración 5

> Esta iteración agrega una idea nueva: la suite ya no verifica solo
> **comportamiento**, también verifica **diseño**. Los tests marcados
> `principios` comprueban LSP, OCP y DIP. Esta guía explica los
> marcadores, las fixtures parametrizadas, los dobles de prueba y la
> medición de cobertura.

Documento hermano: `TDD_ITERACION_05.md` (el contrato). Se dan por
sabidas las guías de las iteraciones 3 y 4.

---

## 1. Correr la suite

```bash
python -m pip install -r requirements.txt
python -m pytest -q                    # toda la suite
python -m pytest -m principios         # solo verificaciones de diseño
python -m pytest -m "not principios"   # solo comportamiento
```

`requirements.txt` fija las dependencias del proyecto:

```
pytest>=8.0
pytest-cov>=5.0
```

---

## 2. Marcadores (`markers`)

Un marcador es una etiqueta que le ponés a un test para poder
filtrarlo después.

```python
@pytest.mark.principios
def test_cuenta_declara_sus_metodos_abstractos():
    esperados = {"tipo", "_validar_extraccion", "cierre_de_periodo"}
    assert esperados <= set(Cuenta.__abstractmethods__)
```

Se declara en `pytest.ini`:

```ini
[pytest]
python_files = test.py test_*.py
testpaths = . tests
markers =
    principios: verifica una propiedad de diseño (LSP, OCP, DIP), no un comportamiento
addopts = -q --strict-markers
```

- **`markers =`**: lista de marcadores válidos, con su descripción.
- **`--strict-markers`**: si usás un marcador que no está declarado
  (un `@pytest.mark.principos` mal escrito, sin la `i`), la suite
  **falla** en vez de aceptarlo en silencio y no encontrarlo nunca
  con el filtro `-m`.
- **`-m principios`** corre solo los marcados; **`-m "not principios"`**
  corre el resto.

Para qué sirve la separación: los tests de comportamiento son los que
mirás mientras programás; los de diseño son un candado que salta
cuando alguien "arregla" algo rompiendo la arquitectura (por ejemplo,
duplicando `extraer` en una subclase).

---

## 3. Fixtures parametrizadas — un test, todos los tipos

En la Iteración 3 parametrizabas el **test**. Acá se parametriza la
**fixture**:

```python
CLASES_CONCRETAS = (CuentaAhorro, CuentaCorriente, CuentaSueldo)

@pytest.fixture(params=CLASES_CONCRETAS, ids=lambda c: c.__name__)
def cualquier_cuenta(request, titular):
    return request.param("00000000000017", titular, 10_000)
```

- **`params=...`**: la fixture se "multiplica" por cada elemento.
- **`request.param`**: dentro de la fixture, el elemento actual.
- **`ids=lambda c: c.__name__`**: cómo se llama cada variante en la
  salida.

Un test que reciba `cualquier_cuenta` se ejecuta **una vez por tipo**:

```python
def test_el_deposito_se_comporta_igual_en_toda_la_jerarquia(cualquier_cuenta):
    saldo_previo = cualquier_cuenta.saldo
    cualquier_cuenta.depositar(500)
    assert cualquier_cuenta.saldo == saldo_previo + 500
```

```
test_el_deposito_se_comporta_igual[CuentaAhorro]     PASSED
test_el_deposito_se_comporta_igual[CuentaCorriente]  PASSED
test_el_deposito_se_comporta_igual[CuentaSueldo]     PASSED
```

Esto **es** el test de LSP: la misma prueba tiene que pasar para
cualquier subclase. Cuando agregues un tipo de cuenta, lo sumás a
`CLASES_CONCRETAS` y toda la batería se le aplica sola, sin escribir
un test más. Lo mismo con `IMPLEMENTACIONES_REPO` para el
repositorio.

---

## 4. Verificar diseño con `inspect` y `dataclasses`

### Clases abstractas

```python
import inspect

@pytest.mark.principios
@pytest.mark.parametrize("abstracta", [Persona, Cuenta, RepositorioCuentas],
                         ids=lambda c: c.__name__)
def test_las_clases_base_no_se_instancian(abstracta):
    assert inspect.isabstract(abstracta)
    with pytest.raises(TypeError):
        abstracta()
```

- `inspect.isabstract(X)` → `True` si `X` tiene métodos abstractos
  sin implementar.
- `X.__abstractmethods__` → el `frozenset` de esos nombres. Una
  concreta bien hecha lo tiene vacío:

```python
@pytest.mark.parametrize("clase", CLASES_CONCRETAS, ids=lambda c: c.__name__)
def test_las_clases_concretas_implementan_todo(clase):
    assert clase.__abstractmethods__ == frozenset()
```

### Leer el código fuente de un método (OCP)

```python
@pytest.mark.principios
def test_el_cierre_de_mes_no_pregunta_por_el_tipo():
    codigo = inspect.getsource(Banco.cierre_de_mes)

    assert "isinstance" not in codigo
    assert "TIPO" not in codigo
```

`inspect.getsource` te da el texto del método. Si aparece
`isinstance` o una comparación por `TIPO`, es que `cierre_de_mes`
está preguntando "¿qué tipo de cuenta sos?" en vez de mandar el mismo
mensaje a todas — eso viola OCP. Es un test un poco tramposo (mira
texto, no comportamiento), pero es la forma práctica de blindar la
regla.

### `dataclass` inmutable

```python
import dataclasses

def test_movimiento_es_una_dataclass():
    assert dataclasses.is_dataclass(Movimiento)


def test_movimiento_es_inmutable():
    movimiento = Movimiento("DEPOSITO", 100, 100)
    with pytest.raises(dataclasses.FrozenInstanceError):
        movimiento.monto = 999


def test_cada_movimiento_tiene_su_propia_fecha():
    primero = Movimiento("DEPOSITO", 100, 100)
    segundo = Movimiento("DEPOSITO", 100, 200)
    assert primero.fecha_hora != segundo.fecha_hora
```

- `FrozenInstanceError` es la excepción de un `@dataclass(frozen=True)`
  cuando intentás reasignar un campo.
- El último test atrapa un error clásico: usar `field(default=...)` en
  vez de `field(default_factory=...)` para la fecha. Con `default`,
  todos los movimientos comparten **la misma** fecha (la del momento
  de importar la clase); con `default_factory`, cada uno llama a la
  función y saca la suya.

---

## 5. Dobles de prueba (test doubles)

Como el `Banco` recibe el repositorio inyectado (DIP), en un test le
podés pasar uno **falso** que se porta distinto a propósito.

### Un doble que falla

```python
def test_el_banco_propaga_el_error_del_repositorio(titular):
    class RepositorioQueFalla(RepositorioMemoria):
        def agregar(self, cuenta):
            raise CuentaDuplicadaError("almacenamiento no disponible")

    banco = Banco("Banco UTN", RepositorioQueFalla())

    with pytest.raises(CuentaDuplicadaError):
        banco.abrir_cuenta("AHORRO", titular)
```

Comprueba que el `Banco` **no se traga** el error del repositorio: lo
deja subir. Sin inyección de dependencia no habría forma de provocar
ese fallo.

### Un espía que cuenta llamadas

```python
def test_el_banco_consulta_el_repositorio_al_transferir(titular):
    class RepositorioEspia(RepositorioMemoria):
        def __init__(self):
            super().__init__()
            self.llamadas_a_obtener = 0

        def obtener(self, cbu):
            self.llamadas_a_obtener += 1
            return super().obtener(cbu)

    espia = RepositorioEspia()
    banco = Banco("Banco UTN", espia)
    origen = banco.abrir_cuenta("AHORRO", titular, 1000)
    destino = banco.abrir_cuenta("AHORRO", titular, 0)
    espia.llamadas_a_obtener = 0

    banco.transferir(origen.cbu, destino.cbu, 500)

    assert espia.llamadas_a_obtener == 2
```

Verifica **cómo** el `Banco` usa la abstracción: una transferencia
pide dos cuentas al repositorio, ni una más.

Los dos dobles heredan de `RepositorioMemoria` y redefinen **un**
método. No hace falta ninguna librería de mocking.

---

## 6. El contrato compartido del repositorio

Los tests de `test_un_repositorio_...` reciben la fixture
`repositorio` (parametrizada con `IMPLEMENTACIONES_REPO`). Hoy hay una
sola implementación, pero el día que agregues `RepositorioArchivo`,
lo sumás a la tupla y **toda** la batería de contrato
(`agregar` registra, `obtener` inexistente falla, `listar` devuelve
copia, no se duplica un CBU, solo acepta cuentas) se ejecuta sobre la
nueva sin escribir un test. Eso es ISP + LSP aplicados al testing.

---

## 7. Cobertura (`pytest-cov`)

```bash
python -m pytest --cov=banco --cov-report=term-missing
```

- `--cov=banco`: medí qué líneas del paquete `banco` ejecutan los
  tests.
- `--cov-report=term-missing`: listá en la terminal las líneas **no**
  cubiertas.

La cobertura te dice qué código **nadie prueba**; no te dice que las
pruebas sean buenas. Un 100 % con `assert` flojos no vale nada.
Usalo para encontrar ramas olvidadas (un `except` que nunca se
dispara en ningún test), no como número para exhibir.

---

## 8. Cómo escribir tus tests en `tests/`

Igual que en la Iteración 4, más:

1. **Un test de diseño se marca `@pytest.mark.principios`** y va,
   idealmente, a `test_principios.py`.
2. **Si probás una regla que vale para todos los tipos de cuenta**,
   usá `cualquier_cuenta` en vez de elegir uno.
3. **Si necesitás un repositorio que se porte raro**, heredá de
   `RepositorioMemoria` y redefiní el método justo.
4. **No dupliques el contrato del repositorio** por implementación:
   sumá la clase a la tupla parametrizada.

---

## 9. Checklist

- [ ] `python -m pytest -q` pasa entero.
- [ ] `python -m pytest -m principios` pasa (el diseño se respeta).
- [ ] No hay marcadores sin declarar (`--strict-markers` no se queja).
- [ ] Los tests que valen para varios tipos usan la fixture
      parametrizada, no un tipo suelto.
- [ ] Los dobles de prueba heredan de la clase real y redefinen lo
      mínimo.
- [ ] Un tipo o implementación nuevos se agregan a la tupla
      (`CLASES_CONCRETAS`, `IMPLEMENTACIONES_REPO`) y heredan la
      batería.
- [ ] Mediste cobertura y revisaste las líneas que faltan, no el
      porcentaje.
