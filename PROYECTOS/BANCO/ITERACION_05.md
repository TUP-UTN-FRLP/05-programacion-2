# Proyecto Integrador Banco — Iteración 5 (final)

## Introducción

Esta es la iteración final del proyecto. No agrega funcionalidad nueva
importante: **mejora el diseño** de lo que ya existe, aplicando todo lo del
capítulo, y deja el sistema en condiciones de servir de base al próximo proyecto
integrador con Django.

Cinco cosas cambian:

- **`Cuenta` y `Persona` pasan a ser abstractas** (`ABC`): no se pueden
  instanciar. Solo las clases concretas existen como objetos;
- **aparece `CuentaSueldo`**, un tercer tipo de cuenta, y se agrega **sin tocar
  el código existente** (demostración de OCP);
- **`Movimiento` pasa a ser `@dataclass(frozen=True)`**: la misma clase en un
  tercio de las líneas, y realmente inmutable;
- **aparece el `Repositorio` abstracto**: `Banco` deja de guardar el `dict`
  directamente y delega en un repositorio (demostración de DIP);
- **type hints en toda la jerarquía** y `assert` que verifican los principios en
  tiempo de ejecución.

---

## Qué cambia respecto de la Iteración 4

| Tema | Iteración 4 | Iteración 5 |
| --- | --- | --- |
| Clases base | instanciables (limitación conocida) | abstractas con `ABC` |
| `extraer()` | sobrescrita en cada subclase | escrita una vez en la base, con un paso abstracto |
| Tipos de cuenta | 2 | 3 (`CuentaSueldo`) |
| `Movimiento` | ~60 líneas escritas a mano | `@dataclass(frozen=True)`, ~15 líneas |
| Inmutabilidad | por convención (sin setters) | garantizada por el lenguaje (`FrozenInstanceError`) |
| Almacenamiento | `dict` dentro de `Banco` | `RepositorioCuentas` inyectado |
| Tipos | implícitos | anotados en toda la jerarquía |
| Verificación de diseño | revisión humana | `assert` + tests de contrato |

---

## Objetivo de la Iteración 5

```text
        Persona (ABC)                        Cuenta (ABC)
             │                                    │
     ┌───────┴────────┐              ┌────────────┼────────────┐
     ▼                ▼              ▼            ▼            ▼
PersonaFisica   PersonaJuridica  CuentaAhorro  CuentaCorriente  CuentaSueldo


        Banco  ──────depende de─────►  RepositorioCuentas (ABC)
                                                 ▲
                                                 │ implementa
                                        RepositorioMemoria
```

---

## Conceptos que se trabajan

- clases abstractas con `abc.ABC` y `@abstractmethod`;
- property abstracta;
- método plantilla: la clase base define el algoritmo y delega un paso;
- `@dataclass`, `frozen=True`, `field(default_factory=...)`, `__post_init__`;
- type hints: `str`, `float`, `list[Movimiento]`, `Optional`, `TYPE_CHECKING`;
- inyección de dependencias por constructor;
- principios de diseño:
  - **OCP** (abierto/cerrado): abierto a la extensión, cerrado a la
    modificación;
  - **LSP** (sustitución de Liskov): una subclase puede reemplazar a su base;
  - **DIP** (inversión de dependencias): depender de abstracciones, no de
    implementaciones;
- `assert` como verificación ejecutable de un invariante de diseño.

---

## Importante: qué NO buscamos

- persistencia en archivos o base de datos;
- Django, Flask, FastAPI, interfaz gráfica o frontend;
- concurrencia, hilos ni asincronismo;
- herencia múltiple en el dominio (sigue reservada a los errores);
- metaclases, decoradores propios ni `__slots__`.

> El `RepositorioMemoria` guarda todo en memoria, igual que la Iteración 4. La
> ganancia no es funcional: es que el día que aparezca un `RepositorioDjango`,
> el `Banco` no se entera. Ese es el trabajo del próximo proyecto.

---

## 1. Estructura final del proyecto

```text
main.py                    # menú de consola
banco/
    __init__.py            # reexporta lo público del paquete
    errores.py
    validaciones.py
    personas.py            # Persona (ABC), PersonaFisica, PersonaJuridica
    movimientos.py         # Movimiento (dataclass frozen)
    cuentas.py             # Cuenta (ABC), CuentaAhorro, CuentaCorriente, CuentaSueldo
    banco.py               # clase Banco
    repositorios.py        # RepositorioCuentas (ABC), RepositorioMemoria
test.py                    # contrato de la cátedra
tests/
    __init__.py
    conftest.py
    test_personas.py
    test_cuentas.py
    test_banco.py
    test_repositorios.py
    test_principios.py     # LSP y OCP verificados automáticamente
pytest.ini
requirements.txt
README.md                  # del grupo
.gitignore
```

Los módulos de la Iteración 4 se mueven adentro del paquete `banco/`, sin
cambiar su contenido, en un commit propio. Las importaciones internas pasan a
ser relativas:

```python
# banco/cuentas.py
from .errores import SaldoInsuficienteError
from .movimientos import Movimiento
from .validaciones import validar_monto
```

Y desde afuera, absolutas:

```python
# main.py
from banco import Banco, CuentaAhorro, PersonaFisica
```

Para que esa última línea funcione, `banco/__init__.py` reexporta:

```python
from .banco import Banco
from .cuentas import Cuenta, CuentaAhorro, CuentaCorriente, CuentaSueldo
from .movimientos import Movimiento
from .personas import Persona, PersonaFisica, PersonaJuridica
from .repositorios import RepositorioCuentas, RepositorioMemoria

__all__ = [...]
```

---

## 2. Clases abstractas

### `Persona` abstracta

```python
from abc import ABC, abstractmethod


class Persona(ABC):
    @property
    @abstractmethod
    def identificacion(self) -> str:
        """Identificador legible del titular (DNI o CUIT)."""
```

Al terminar, esto debe fallar:

```python
Persona("Ana")     # TypeError: Can't instantiate abstract class Persona
```

Es la limitación que se anotó en la Iteración 3 y que recién ahora se puede
resolver. La property `identificacion` deja de devolver
`"SIN IDENTIFICACION"`: ese valor era un parche para una clase que no debería
haber existido como objeto.

Python impide la instanciación solo si la clase hereda de `ABC` **y** tiene al
menos un método marcado con `@abstractmethod`.

### `Cuenta` abstracta

```python
class Cuenta(ABC):
    TIPO: str = "Cuenta"

    @property
    @abstractmethod
    def tipo(self) -> str: ...

    @abstractmethod
    def _validar_extraccion(self, monto: float) -> None:
        """Lanza la excepción correspondiente si esta cuenta no permite extraer."""

    @abstractmethod
    def cierre_de_periodo(self) -> float:
        """Aplica la regla de fin de mes del tipo de cuenta. Devuelve el ajuste."""
```

### El refactor de `extraer()`

En las iteraciones 3 y 4, cada subclase sobrescribía `extraer()` entera. Eso
duplicaba la validación del monto, la actualización del saldo y el registro del
movimiento. Ahora `extraer()` se escribe **una sola vez** en la clase base:

```python
def extraer(self, monto: float) -> float:
    monto = validar_monto(monto)
    self._verificar_activa()
    self._validar_extraccion(monto)      # <- único paso que varía
    self.__saldo -= monto
    self._registrar("EXTRACCION", monto)
    return self.__saldo
```

Cada subclase implementa solo `_validar_extraccion()`:

| Clase | Regla |
| --- | --- |
| `CuentaAhorro` | `monto > saldo` → `SaldoInsuficienteError` |
| `CuentaCorriente` | `saldo - monto < -limite` → `LimiteDescubiertoExcedidoError` |
| `CuentaSueldo` | `monto > saldo` → `SaldoInsuficienteError` |

Esto se llama **método plantilla**: la base fija el algoritmo, la subclase
completa un paso. Verificar después del refactor:

```python
assert "extraer" not in CuentaAhorro.__dict__
assert "extraer" not in CuentaCorriente.__dict__
assert "extraer" not in CuentaSueldo.__dict__
```

Ninguna subclase define `extraer`: todas la heredan.

### `cierre_de_periodo()`

Reemplaza a `liquidar_interes()` y `cobrar_mantenimiento()`, que eran métodos
distintos con nombres distintos. Ahora todas las cuentas responden al mismo
mensaje:

| Clase | Qué hace | Movimiento |
| --- | --- | --- |
| `CuentaAhorro` | acredita `saldo * tasa_interes` | `"INTERES"` |
| `CuentaCorriente` | descuenta `COSTO_MANTENIMIENTO` | `"MANTENIMIENTO"` |
| `CuentaSueldo` | aplica retención sobre el excedente del tope | `"RETENCION"` o nada |

Con eso, el `Banco` puede hacer:

```python
def cierre_de_mes(self) -> None:
    for cuenta in self.listar_cuentas_activas():
        cuenta.cierre_de_periodo()
```

sin preguntar de qué tipo es ninguna. Comparar con lo que había que escribir en
la Iteración 4.

---

## 3. `CuentaSueldo`: la prueba del OCP

```python
CuentaSueldo(numero, titular, saldo_inicial=0, tope_libre_retencion=3_000_000)
```

Reglas:

- **no cobra mantenimiento**;
- **no permite descubierto** (igual que la caja de ahorro);
- tiene un **tope de saldo libre de retención**: en el cierre de período, si el
  saldo supera el tope, se retiene un porcentaje sobre el **excedente**;
- el titular debe ser una `PersonaFisica`: una empresa no cobra sueldo →
  `ErrorDeTipo`;
- `TIPO = "Cuenta Sueldo"`;
- atributo de clase `ALICUOTA_RETENCION = 0.006`.

```text
excedente = max(0, saldo - tope_libre_retencion)
retencion = excedente * ALICUOTA_RETENCION
```

Si el excedente es `0`, no se registra ningún movimiento.

### La consigna del OCP

`CuentaSueldo` debe agregarse **sin modificar ninguna línea** de:

- `Cuenta`, `CuentaAhorro` ni `CuentaCorriente`;
- `Movimiento` (salvo agregar `"RETENCION"` a `TIPOS`);
- `Banco`, salvo **una línea** en el diccionario `TIPOS_DE_CUENTA`;
- `main.py`;
- los tests existentes.

Antes de escribirla, hacer `git log` y anotar el hash del último commit. Al
terminar, `git diff <hash> --stat` debe mostrar archivos nuevos y esas dos
líneas. Ese diff es la evidencia del principio y forma parte de la entrega.

> Si para agregar `CuentaSueldo` hay que tocar `Cuenta`, significa que la
> abstracción no era la correcta. Es información valiosa, no un fracaso:
> anotarlo en el README con lo que habría que haber previsto.

---

## 4. `Movimiento` como `dataclass`

```python
from dataclasses import dataclass, field
from datetime import datetime
from zoneinfo import ZoneInfo

_ZONA_ARGENTINA = ZoneInfo("America/Argentina/Buenos_Aires")


def _ahora_argentina() -> datetime:
    return datetime.now(_ZONA_ARGENTINA)


@dataclass(frozen=True)
class Movimiento:
    tipo: str
    monto: float
    saldo_posterior: float
    fecha_hora: datetime = field(default_factory=_ahora_argentina)

    def __post_init__(self) -> None:
        validar_tipo_movimiento(self.tipo)
        validar_monto(self.monto)
```

La `default_factory` sigue siendo la hora argentina (UTC−3) que se fijó en la
Iteración 4: se envuelve `datetime.now(_ZONA_ARGENTINA)` en una función chica
porque `field(default_factory=...)` espera un invocable sin argumentos.

Qué escribe el decorador por nosotros: `__init__`, `__repr__`, `__eq__`.

Qué aporta `frozen=True`: asignar un atributo lanza
`dataclasses.FrozenInstanceError`. En la Iteración 4 la inmutabilidad era una
**convención** (no escribíamos setters); ahora es una **garantía del lenguaje**.

Puntos a resolver:

- **`default_factory` y no `default`**: `fecha_hora: datetime = datetime.now()`
  evaluaría `now()` **una sola vez**, al definir la clase, y todos los
  movimientos tendrían la misma hora. Probarlo para verlo;
- **`__post_init__`**: es el único lugar donde se pueden validar los datos,
  porque el `__init__` lo genera el decorador;
- **validar en una clase `frozen`**: si una validación necesita *normalizar* un
  valor, no se puede asignar directamente. Buscar `object.__setattr__` y
  documentar la decisión;
- **cambio de contrato respecto de la Iteración 4:** ahora `fecha_hora` **se
  puede** pasar por parámetro. En la Iteración 4 estaba prohibido para que
  nadie falseara la hora de una operación; como campo de una `dataclass`
  necesita ser un parámetro más. La garantía se mueve de lugar: el único código
  que crea movimientos es `Cuenta._registrar()`, que nunca la pasa;
- `__str__` se sigue escribiendo a mano: el `__repr__` automático sirve para
  depurar, no para mostrarle a un usuario;
- `FrozenInstanceError` **no** es una excepción del dominio y no hereda de
  `BancoError`. Decidir en grupo si se traduce o se deja pasar.

Comparar el archivo antes y después con `git diff`: es la demostración más
clara de la iteración.

---

## 5. `repositorios.py`: el patrón repositorio

### La abstracción

```python
class RepositorioCuentas(ABC):
    @abstractmethod
    def agregar(self, cuenta: "Cuenta") -> None: ...

    @abstractmethod
    def obtener(self, cbu: str) -> "Cuenta": ...

    @abstractmethod
    def listar(self) -> list["Cuenta"]: ...

    @abstractmethod
    def existe(self, cbu: str) -> bool: ...

    @abstractmethod
    def cantidad(self) -> int: ...
```

Es la misma herramienta de la sección 2 aplicada a otra cosa: acá no define una
familia de entidades, define un **contrato de servicio**.

`obtener()` con un CBU inexistente lanza `CuentaInexistenteError`: la traducción
del error es responsabilidad del repositorio, no de quien lo usa.

### La implementación en memoria

```python
class RepositorioMemoria(RepositorioCuentas):
    def __init__(self) -> None:
        self.__cuentas: dict[str, Cuenta] = {}
```

Es exactamente el `dict` que tenía adentro el `Banco` en la Iteración 4, mudado
de lugar.

### El `Banco` inyectado

```python
class Banco:
    def __init__(self, nombre: str,
                 repositorio: RepositorioCuentas | None = None) -> None:
        self.__nombre = validar_nombre_banco(nombre)
        self.__repositorio = repositorio or RepositorioMemoria()
```

Reglas:

- `Banco` **no** debe contener ningún `dict`, `list` ni `set` de cuentas;
- si se pasa un `repositorio` que no es un `RepositorioCuentas` → `ErrorDeTipo`;
- todos los métodos del `Banco` pasan por el repositorio.

### Por qué esto es DIP

Antes: `Banco` (política) dependía de `dict` (detalle de implementación).
Ahora: `Banco` depende de `RepositorioCuentas` (abstracción), y
`RepositorioMemoria` también depende de esa abstracción. Los dos apuntan al
mismo lugar: la dependencia quedó **invertida**.

La consecuencia práctica se ve en los tests: se puede pasar un repositorio falso
que cuente llamadas o que simule un fallo, sin tocar el `Banco`.

> El próximo proyecto integrador reemplaza `RepositorioMemoria` por uno que
> hable con la base de datos de Django. Si esta iteración está bien hecha, el
> dominio no cambia una línea.

---

## 6. Type hints

Anotar toda la jerarquía: parámetros, valores de retorno y atributos de clase.

```python
class CuentaAhorro(Cuenta):
    TIPO: str = "Caja de Ahorro"
    TASA_POR_DEFECTO: float = 0.01

    def __init__(self, numero: str, titular: Persona,
                 saldo_inicial: float = 0,
                 tasa_interes: float = TASA_POR_DEFECTO) -> None: ...

    def cierre_de_periodo(self) -> float: ...

    def historial(self) -> list[Movimiento]: ...
```

Puntos a tener en cuenta:

- un método que no devuelve nada se anota `-> None`;
- `float` cubre también a `int` según la convención de tipos de Python
  (*numeric tower*); no hace falta `int | float`;
- para evitar importaciones circulares en las anotaciones se usa
  `from __future__ import annotations` o comillas: `def agregar(self, cuenta:
  "Cuenta")`;
- **las anotaciones no validan nada en ejecución**. Escribir `monto: float` no
  reemplaza a `validar_monto()`. Son documentación verificable por herramientas,
  no un control.

Verificación opcional con `mypy`:

```bash
python -m pip install mypy
python -m mypy banco/
```

No es obligatorio que pase sin advertencias, pero conviene mirar lo que reporta.

---

## 7. Verificaciones con `assert`

En `main.py` o en un módulo `verificaciones.py`, incluir asserts que comprueben
los principios. Se ejecutan al arrancar y documentan el diseño en código.

### LSP

```python
CONCRETAS = (CuentaAhorro, CuentaCorriente, CuentaSueldo)

for clase in CONCRETAS:
    assert issubclass(clase, Cuenta)
    assert "extraer" not in clase.__dict__, (
        f"{clase.__name__} sobrescribe extraer(): duplica el algoritmo base"
    )
    assert "depositar" not in clase.__dict__
    assert clase.TIPO != Cuenta.TIPO, f"{clase.__name__} no redefinió TIPO"
```

Y la sustitución en acción:

```python
cuentas = [ahorro, corriente, sueldo]
for cuenta in cuentas:
    saldo_previo = cuenta.saldo
    cuenta.depositar(1000)
    assert cuenta.saldo == saldo_previo + 1000
    cuenta.cierre_de_periodo()      # ninguna falla, todas responden
```

### OCP

```python
assert set(Banco.TIPOS_DE_CUENTA) == {"AHORRO", "CORRIENTE", "SUELDO"}
assert all(issubclass(c, Cuenta) for c in Banco.TIPOS_DE_CUENTA.values())
```

### Abstracción

```python
for abstracta in (Persona, Cuenta, RepositorioCuentas):
    try:
        abstracta()
    except TypeError:
        pass
    else:
        raise AssertionError(f"{abstracta.__name__} no es abstracta")
```

> `assert` **no** reemplaza a las validaciones ni a las excepciones del
> dominio. Un `assert` documenta algo que el programador garantiza que es
> cierto; una excepción maneja algo que el usuario puede provocar. Además,
> `python -O` desactiva los `assert`: nunca poner adentro una regla de negocio.

---

## 8. `main.py`

Se conserva el menú de la Iteración 4, con tres cambios:

- se agrega `"SUELDO"` a las opciones de apertura (una línea);
- se agrega la opción "Cierre de mes", que llama a `banco.cierre_de_mes()`;
- el banco se construye inyectando el repositorio:

```python
banco = Banco("Banco UTN", RepositorioMemoria())
```

Nada más cambia. Que el menú casi no se toque es parte del resultado.

---

## 9. Qué debe observarse al finalizar

- `Persona()`, `Cuenta()` y `RepositorioCuentas()` lanzan `TypeError`;
- ninguna subclase de `Cuenta` define `extraer` ni `depositar`;
- las tres cuentas responden a `cierre_de_periodo()` con reglas distintas;
- el `git diff` de `CuentaSueldo` toca solo archivos nuevos y dos líneas;
- `movimiento.monto = 999` lanza `FrozenInstanceError`;
- `Banco` no contiene ninguna colección de cuentas;
- reemplazar `RepositorioMemoria` por otro repositorio no cambia el `Banco`;
- todos los métodos públicos están anotados;
- los `assert` de principios pasan;
- `python -m pytest -q` pasa completo.

---

## 10. Decisiones de diseño para pensar

### 1. ¿Qué tan abstracta debe ser la base?

`Cuenta` tiene tres métodos abstractos. ¿Y si tuviera diez? ¿Cuántos puede
tener antes de que agregar un tipo nuevo sea más trabajo que copiar y pegar?

### 2. `dataclass` para las demás clases

`Movimiento` quedó bien como `dataclass`. ¿Y `Cuenta`? ¿Y `PersonaFisica`?
Probar y explicar por qué **no** conviene (pista: encapsulamiento, properties de
solo lectura, atributos con doble guion bajo).

### 3. El repositorio y las personas

Se hizo un repositorio de cuentas. ¿Hace falta uno de personas? ¿Dónde viven
hoy las personas? ¿Es un problema?

### 4. Los `float` y el dinero

`0.1 + 0.2` no da `0.3`. En este proyecto lo aceptamos. Investigar
`decimal.Decimal` y estimar qué habría que cambiar para migrar. **No
implementarlo**: escribir la respuesta en el README.

### 5. Lo que viene

Mirar `RepositorioCuentas` y pensar cómo sería un `RepositorioDjango`. ¿Qué
método sería una consulta al ORM? ¿Qué pasa con `obtener()` cuando el objeto no
está en memoria sino en una tabla?

---

## 11. Forma de trabajo individual

Rama:

```text
iteracion-05/nombre-apellido
```

Orden sugerido:

1. mudar los módulos al paquete `banco/`, sin cambiar lógica, y verificar que la
   suite de la Iteración 4 sigue pasando;
2. convertir `Persona` y `Cuenta` en abstractas y refactorizar `extraer()` como
   método plantilla;
3. unificar `liquidar_interes()` y `cobrar_mantenimiento()` en
   `cierre_de_periodo()`;
4. **anotar el hash del commit** y agregar `CuentaSueldo`;
5. convertir `Movimiento` en `dataclass(frozen=True)`;
6. extraer el repositorio e inyectarlo en `Banco`;
7. agregar los type hints;
8. escribir los `assert` de principios y los tests de contrato;
9. escribir el README del grupo.

Los pasos 2 y 6 son refactorizaciones: la suite debe seguir pasando **durante**
el cambio, no solo al final. Si hay que romper diez tests para avanzar, algo se
está reescribiendo en lugar de refactorizarse.

---

## 12. Commits sugeridos

```text
Reorganiza los modulos en el paquete banco
Convierte Persona en clase abstracta
Convierte Cuenta en clase abstracta
Refactoriza extraer como metodo plantilla
Unifica el cierre de periodo de las cuentas
Agrega CuentaSueldo sin modificar las clases existentes
Convierte Movimiento en dataclass inmutable
Extrae RepositorioCuentas e implementa RepositorioMemoria
Inyecta el repositorio en Banco
Agrega type hints a la jerarquia
Agrega verificaciones de LSP y OCP
Agrega tests de principios y de repositorio
Agrega README del proyecto
```

---

## 13. README del grupo

La entrega final incluye un `README.md` escrito por el grupo, con:

- descripción del sistema en un párrafo;
- instrucciones de instalación y ejecución;
- cómo correr las pruebas;
- el diagrama de clases del modelo final;
- las decisiones de diseño tomadas y las alternativas descartadas;
- el `git diff --stat` que demuestra el OCP al agregar `CuentaSueldo`;
- limitaciones conocidas (empezando por: no hay persistencia);
- integrantes y qué iteración lideró cada uno.

Es la primera vez que se pide documentación para un lector externo. Se evalúa
que alguien ajeno al grupo pueda clonar el repositorio y ponerlo a funcionar
siguiendo solo ese archivo.

---

## 14. Entrega final del proyecto

Rama `integracion/iteracion-05`, Pull Request hacia `main`.

Demo de cinco minutos:

1. `python -m pytest -q` en verde, incluidos los tests de principios;
2. intento de instanciar `Cuenta` y `Persona`: falla;
3. apertura de las tres clases de cuenta desde el menú;
4. operaciones y transferencia entre dos tipos distintos;
5. cierre de mes: las tres cuentas responden distinto al mismo llamado;
6. `movimiento.monto = 999`: `FrozenInstanceError`;
7. el `git diff --stat` de `CuentaSueldo`;
8. explicación de qué habría que cambiar para pasar a Django.

---

## Criterio central

La pregunta final del proyecto es:

> ¿Cuánto código existente hubo que modificar para agregar un tipo de cuenta
> nuevo, y cuánto habría que modificar para cambiar dónde se guardan los datos?

La respuesta buscada es: **dos líneas y ninguna**.

Y, sobre todo, cada integrante debe poder decir:

> Implementé cada etapa del proyecto, comparé mi solución con otras, participé
> en revisiones, discutí decisiones de diseño y colaboré en la construcción de
> la versión integrada de mi grupo.
