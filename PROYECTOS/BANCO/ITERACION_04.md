# Proyecto Integrador Banco — Iteración 4

## Introducción

Esta es la iteración más grande del proyecto. Hasta acá tenemos entidades bien
modeladas, pero no tenemos un **sistema**: las cuentas existen sueltas dentro
del escenario, nadie las administra, y una cuenta sabe su saldo pero no sabe
**cómo llegó** a ese saldo.

Aparecen cuatro cosas nuevas y una reorganización:

- la clase **`Movimiento`**: registra cada operación con fecha, tipo, monto y
  saldo posterior. Cada cuenta guarda su historial;
- la clase **`Banco`**: el gestor, con ABM completo de cuentas y generación
  automática de **CBU** al abrir cada una;
- la operación **`transferir`**: mueve dinero entre dos cuentas de forma
  **atómica** (o pasa entera o falla entera);
- la **baja lógica**: cerrar una cuenta no la borra, la marca como inactiva; el
  historial persiste;
- el proyecto **se reorganiza en varios archivos**, con una jerarquía de errores
  propia.

Además, el trabajo con `pytest` —que arrancó en la Iteración 3— se amplía:
la suite se parte en varios archivos dentro de `tests/`, con un `conftest.py`
para las fixtures compartidas, y se mide cobertura.

---

## Qué cambia respecto de la Iteración 3

| Tema | Iteración 3 | Iteración 4 |
| --- | --- | --- |
| Historial | no existe | cada cuenta guarda una lista de `Movimiento` |
| Fechas | prohibidas | `datetime` en cada movimiento |
| Administración | ninguna | clase `Banco` con ABM |
| Identificación de la cuenta | número de 14 dígitos escrito a mano | número generado + **CBU de 22 dígitos** |
| Transferencias | no existen | `Banco.transferir()`, atómica |
| Cierre de cuenta | no existe | baja lógica: `activa` / `inactiva` |
| Errores | `ValueError` / `TypeError` | jerarquía propia en `errores.py` |
| Archivos | `banco.py` + `validaciones.py` | 7 módulos |
| Pruebas | `test.py` + un archivo propio | `test.py` + carpeta `tests/` con `conftest.py` |
| Verificación | `pytest` (suite en la raíz) | `pytest` + cobertura |

---

## Objetivo de la Iteración 4

```text
                    Banco
                      │
                      │ administra
                      ▼
                   Cuenta ──── titular ────► Persona
                      │
                      │ registra
                      ▼
                  Movimiento
```

`Banco` es el punto de entrada único al sistema: nada de afuera abre cuentas
por su cuenta. `main.py` habla **solo** con `Banco`.

---

## Conceptos que se trabajan

- excepciones personalizadas: una clase que hereda de `Exception`;
- jerarquías de excepciones y captura por clase base;
- herencia múltiple aplicada a excepciones (compatibilidad con `ValueError`);
- `raise ... from ...` (encadenamiento);
- `try` / `except` / `else` / `finally`;
- colecciones de objetos: `list` para el historial, `dict` como índice;
- composición 1 a N (una cuenta tiene muchos movimientos);
- diccionario como despachador de operaciones;
- `@classmethod` y `@staticmethod`;
- métodos especiales de colección: `__len__`, `__contains__`, `__iter__`;
- módulos, importaciones entre archivos propios y dependencias circulares;
- separación entre lógica de negocio e interfaz de usuario;
- `pytest`: ejecución, `assert`, `pytest.raises`, fixtures, `parametrize`;
- ciclo TDD: rojo → verde → refactor.

---

## Importante: qué NO buscamos todavía

- clases abstractas (`ABC`, `@abstractmethod`);
- `@dataclass` ni type hints sistemáticos;
- patrón repositorio;
- persistencia en archivos o base de datos;
- interfaz gráfica, web, Django, Flask o FastAPI;
- concurrencia, hilos ni asincronismo.

> Al cerrar esta iteración todo se sigue perdiendo al terminar el programa. Es
> esperable: el almacenamiento se aborda en la Iteración 5, y la persistencia
> real en el próximo proyecto.

---

## 1. Estructura del proyecto

```text
validaciones.py   # funciones de validación (sin dependencias)
errores.py        # jerarquía de excepciones (sin dependencias)
personas.py       # Persona, PersonaFisica, PersonaJuridica
movimientos.py    # Movimiento
cuentas.py        # Cuenta, CuentaAhorro, CuentaCorriente
banco.py          # clase Banco
main.py           # menú de consola; único archivo con input()
test.py           # contrato de la cátedra (ahora SÍ se ejecuta)
tests/            # pruebas escritas por el grupo
    __init__.py
    test_movimientos.py
    test_banco.py
    test_transferencias.py
pytest.ini
.gitignore
```

Dirección de las dependencias:

```text
main.py ──► banco.py ──► cuentas.py ──► movimientos.py
                │            │              │
                └────────────┴──────────────┴──► validaciones.py ──► errores.py
                             │
                             └──► personas.py
```

Las flechas van en un solo sentido. `cuentas.py` **no** importa `banco.py`.
Si dos módulos se importan mutuamente, Python lanza un `ImportError` en el
arranque: la dependencia circular no es una cuestión de estilo, no compila.

> `banco.py` cambia de contenido: pasa de tener todas las clases a tener solo
> la clase `Banco`. Conviene hacer la mudanza en un commit propio, sin cambiar
> lógica, y verificar que el escenario de la Iteración 3 sigue funcionando
> antes de agregar nada nuevo.

---

## 2. `errores.py`

### Jerarquía

```python
class BancoError(Exception):
    """Raíz de todos los errores del sistema."""


class ErrorDeValidacion(BancoError, ValueError): ...
class ErrorDeTipo(BancoError, TypeError): ...

class NombreInvalidoError(ErrorDeValidacion): ...
class DniInvalidoError(ErrorDeValidacion): ...
class CuitInvalidoError(ErrorDeValidacion): ...
class CbuInvalidoError(ErrorDeValidacion): ...
class MontoInvalidoError(ErrorDeValidacion): ...
class SaldoInicialInvalidoError(ErrorDeValidacion): ...

class ErrorDeOperacion(BancoError): ...
class SaldoInsuficienteError(ErrorDeOperacion): ...
class LimiteDescubiertoExcedidoError(SaldoInsuficienteError): ...
class TransferenciaInvalidaError(ErrorDeOperacion): ...
class CuentaInactivaError(ErrorDeOperacion): ...

class ErrorDeRegistro(BancoError): ...
class CuentaInexistenteError(ErrorDeRegistro): ...
class CuentaDuplicadaError(ErrorDeRegistro): ...
class CuentaConSaldoError(ErrorDeRegistro): ...
```

### Por qué `ErrorDeValidacion` hereda también de `ValueError`

Toda la validación de las iteraciones 2 y 3 lanzaba `ValueError` y `TypeError`.
Si ahora lanzáramos únicamente excepciones nuevas, todo el código —y todos los
casos de `test.py`— que hacía `except ValueError` dejaría de funcionar.

Al heredar de las dos, una `MontoInvalidoError`:

- se captura como `MontoInvalidoError` (preciso);
- se captura como `ErrorDeValidacion` (por categoría);
- se captura como `BancoError` (todo el sistema);
- se sigue capturando como `ValueError` (compatibilidad hacia atrás).

Comprobarlo en el escenario e inspeccionar `MontoInvalidoError.__mro__`.

> Es herencia múltiple, y en el proyecto se usa **solo acá**: es su caso de uso
> más frecuente y menos problemático. Las entidades del dominio siguen usando
> herencia simple.

### Mensajes y datos

Cada excepción se lanza con un mensaje útil, construido en el punto donde
ocurre el problema:

```python
raise SaldoInsuficienteError(
    f"Saldo insuficiente: disponible ${self.saldo:.2f}, "
    f"solicitado ${monto:.2f}"
)
```

Prohibido `raise SaldoInsuficienteError()` sin mensaje.

Las excepciones de operación pueden llevar datos como atributos, para que quien
las capture no tenga que leer el texto:

```python
class SaldoInsuficienteError(ErrorDeOperacion):
    def __init__(self, mensaje, disponible=None, solicitado=None):
        super().__init__(mensaje)
        self.disponible = disponible
        self.solicitado = solicitado
```

### Sustituciones a realizar

No se agrega lógica: cambia **qué** se lanza.

| Situación | Antes | Ahora |
| --- | --- | --- |
| nombre inválido | `ValueError` | `NombreInvalidoError` |
| DNI / CUIT inválido | `ValueError` | `DniInvalidoError` / `CuitInvalidoError` |
| tipo incorrecto | `TypeError` | `ErrorDeTipo` o subclase |
| monto `<= 0` | `ValueError` | `MontoInvalidoError` |
| extracción sin fondos (ahorro) | `ValueError` | `SaldoInsuficienteError` |
| extracción fuera del descubierto | `ValueError` | `LimiteDescubiertoExcedidoError` |
| operar sobre cuenta cerrada | — | `CuentaInactivaError` |

### Encadenamiento

Cuando se traduce un error de bajo nivel a uno del dominio, se conserva la
causa:

```python
try:
    numero = str(dato)
except Exception as error:
    raise CbuInvalidoError("CBU ilegible") from error
```

Ejecutar una vez sin el `from error` y comparar el *traceback*.

---

## 3. `movimientos.py`

```python
Movimiento(tipo, monto, saldo_posterior)
```

Representa una operación **ya ocurrida**. Es un objeto inmutable: se crea y no
se modifica.

### Atributos

```text
__tipo             str, uno de los tipos permitidos
__monto            numérico > 0
__saldo_posterior  numérico (puede ser negativo en cuenta corriente)
__fecha_hora       datetime con zona horaria argentina, lo determina la clase
```

### La fecha y hora las pone el `Movimiento`

Un movimiento registra **cuándo** ocurrió una operación, y ese dato no lo puede
elegir quien la ejecuta: lo fija la clase, en el momento de crear el objeto.

```python
from datetime import datetime
from zoneinfo import ZoneInfo

_ZONA = ZoneInfo("America/Argentina/Buenos_Aires")

# dentro de __init__:
self.__fecha_hora = datetime.now(_ZONA)
```

Se usa `datetime.now(ZoneInfo("America/Argentina/Buenos_Aires"))` y **no**
`datetime.now()` a secas: el banco opera en horario argentino (UTC−3), y la hora
de un movimiento tiene que ser esa aunque el programa corra en un servidor
configurado en otra zona. `zoneinfo` es de la biblioteca estándar desde Python
3.9; no hay que instalar nada.

`Movimiento` **no** recibe la fecha por parámetro en esta iteración: así nadie
puede antedatar ni postdatar una operación.

### Tipos permitidos

Atributo de clase, no texto suelto repetido por el código:

```python
class Movimiento:
    TIPOS = ("DEPOSITO", "EXTRACCION", "TRANSFERENCIA_ENTRADA",
             "TRANSFERENCIA_SALIDA", "INTERES", "MANTENIMIENTO",
             "APERTURA", "CIERRE")
```

Un `tipo` fuera de `TIPOS` → `ErrorDeValidacion`.

### Properties

Las cuatro, de solo lectura. No hay setters: un movimiento registrado no se
edita ni se borra. Ese es el punto de un libro contable.

### `__str__`

```text
[2026-03-14 10:22] DEPOSITO                $  1500.00  ->  saldo $  2500.00
```

Formato libre, pero una lista impresa una por línea debe leerse alineada.

> En la Iteración 5 esta clase se reescribe con `@dataclass(frozen=True)` y
> queda en un tercio de las líneas. Escribirla ahora a mano es lo que va a
> permitir apreciar la diferencia.

---

## 4. Historial en las cuentas

`Cuenta` gana un atributo y tres métodos.

```text
__movimientos   list, empieza vacía
__activa        bool, empieza en True
```

### `_registrar(tipo, monto)`

Método protegido (un solo guion bajo) que crea el `Movimiento` con el saldo
actual y lo agrega a la lista. Lo llaman `depositar()`, `extraer()`,
`liquidar_interes()` y `cobrar_mantenimiento()`.

> Un guion bajo significa "interno, también para las subclases". Dos guiones
> bajos activan *name mangling* y complican el acceso desde las subclases; por
> eso los métodos internos que las subclases necesitan llevan **uno** solo.

### `historial()`

Devuelve una **copia** de la lista:

```python
return list(self.__movimientos)
```

Pensar qué pasaría si se devolviera la lista original y alguien hiciera
`cuenta.historial().clear()`.

### Baja lógica

```text
activa            property de solo lectura
cerrar()          marca la cuenta como inactiva y registra un movimiento "CIERRE"
```

Reglas:

- una cuenta con saldo distinto de `0` no se puede cerrar →
  `CuentaConSaldoError`;
- `depositar()` y `extraer()` sobre una cuenta inactiva →
  `CuentaInactivaError`;
- el historial de una cuenta cerrada **sigue accesible**;
- cerrar una cuenta ya cerrada → `CuentaInactivaError`.

> Por qué baja lógica y no `del`: los movimientos de una cuenta cerrada siguen
> siendo información contable y legal. Borrarlos no es una opción. Es el mismo
> criterio que usa cualquier sistema real con datos históricos.

---

## 5. CBU

Al abrir una cuenta, el banco genera dos identificadores:

```text
numero   14 dígitos   (identificador interno, el de la Iteración 2)
cbu      22 dígitos   (identificador interbancario)
```

### Estructura del CBU

```text
   bloque 1 (8)                 bloque 2 (14)
┌──────────────────┐   ┌──────────────────────────────┐
 285   0100    6      0000000000001   7
 │      │      │           │          │
 │      │      │           │          └─ dígito verificador del bloque 2
 │      │      │           └───────────── numeración de la cuenta (13)
 │      │      └───────────────────────── dígito verificador del bloque 1
 │      └──────────────────────────────── sucursal (4)
 └─────────────────────────────────────── entidad (3)
```

El **bloque 2 es exactamente el número de cuenta de 14 dígitos** que venimos
usando desde la Iteración 2: 13 dígitos de numeración más su verificador.

### Dígitos verificadores

```text
Bloque 1: pesos  7 1 3 9 7 1 3            sobre los 7 primeros dígitos
Bloque 2: pesos  3 9 7 1 3 9 7 1 3 9 7 1 3 sobre los 13 primeros dígitos

dv = (10 - (suma_de_productos % 10)) % 10
```

Ejemplo del bloque 1 con la entidad `285` y la sucursal `0100`:

```text
dígitos    2   8   5   0   1   0   0
pesos      7   1   3   9   7   1   3
producto  14   8  15   0   7   0   0   ->  suma = 44

dv = (10 - (44 % 10)) % 10 = (10 - 4) % 10 = 6   ->  bloque 1 = "28501006"
```

Como la entidad y la sucursal son constantes de la clase `Banco`, el bloque 1
es siempre `"28501006"`. Lo que cambia de una cuenta a otra es el bloque 2.

### Generación

```python
class Banco:
    ENTIDAD = "285"
    SUCURSAL = "0100"

    @classmethod
    def generar_numero_cuenta(cls) -> str: ...

    @classmethod
    def generar_cbu(cls, numero_cuenta) -> str: ...
```

`generar_numero_cuenta` produce 13 dígitos correlativos (con ceros a la
izquierda) y les agrega el verificador. `generar_cbu` antepone el bloque 1 con
su propio verificador.

Pensar por qué son `@classmethod` y no métodos de instancia, y por qué el
resultado es `str` y no `int` (retomar la pregunta de la Iteración 1: ¿qué pasa
con los ceros a la izquierda?).

### Cómo llega el CBU a la cuenta

El CBU es un identificador **interbancario**: lo asigna la entidad, no la
cuenta. Por eso `Cuenta` lo recibe como parámetro **solo por nombre**, con
`None` por defecto:

```python
class Cuenta:
    def __init__(self, numero, titular, saldo_inicial=0, *, cbu=None):
        ...
```

El `*` obliga a que `cbu` se pase con nombre, así los tres parámetros
posicionales de la Iteración 3 no cambian y las subclases siguen recibiendo
`tasa_interes` y `limite_descubierto` en la misma posición de siempre. Cada
subclase reenvía los argumentos con nombre a la base:

```python
class CuentaAhorro(Cuenta):
    def __init__(self, numero, titular, saldo_inicial=0,
                 tasa_interes=TASA_POR_DEFECTO, **kwargs):
        super().__init__(numero, titular, saldo_inicial, **kwargs)
        ...
```

Consecuencia buscada: una cuenta creada fuera del banco tiene `cbu is None`.
Solo `Banco.abrir_cuenta()` le asigna uno. `cbu` es property de solo lectura.

### Validación

```python
validar_cbu(valor)   # -> str de 22 dígitos con ambos verificadores correctos
```

`validar_numero_cuenta` **no cambia**: sigue exigiendo 14 dígitos sin verificar
el dígito de control, para no invalidar los datos de prueba de las iteraciones
anteriores. Es una decisión de compatibilidad, y conviene dejarla comentada en
el código.

---

## 6. `banco.py`: la clase `Banco`

```python
Banco(nombre)
```

### Atributos

```text
__nombre    str no vacío
__cuentas   dict  { cbu (str) -> Cuenta }
```

> ¿Por qué `dict` y no `list`? Buscar una cuenta en una lista obliga a
> recorrerla entera. Con un diccionario el acceso es directo. La clave elegida
> debe ser el identificador natural de la entidad.

### ABM de cuentas

```python
abrir_cuenta(tipo, titular, saldo_inicial=0, **extras) -> Cuenta
buscar_cuenta(cbu) -> Cuenta
listar_cuentas_activas() -> list[Cuenta]
listar_cuentas() -> list[Cuenta]
cerrar_cuenta(cbu) -> Cuenta
```

Reglas:

- `abrir_cuenta` genera el número y el CBU, construye la cuenta del tipo pedido
  y la registra. Devuelve la cuenta creada y registra un movimiento
  `"APERTURA"` si el saldo inicial es mayor que `0`;
- `tipo` es un `str` (`"AHORRO"` / `"CORRIENTE"`); un tipo desconocido →
  `ErrorDeValidacion`;
- los parámetros propios de cada tipo (`tasa_interes`, `limite_descubierto`)
  llegan como argumentos con nombre; pasar `limite_descubierto` a una caja de
  ahorro → `ErrorDeValidacion`;
- `buscar_cuenta` con un CBU no registrado → `CuentaInexistenteError`;
- `listar_cuentas_activas` **no** incluye las cerradas; `listar_cuentas` sí;
- ambas devuelven listas nuevas, nunca la colección interna;
- `cerrar_cuenta` delega en `cuenta.cerrar()`: la cuenta sigue en el
  diccionario.

### La fábrica de cuentas

`abrir_cuenta` **no** debe tener una cadena de `if` sobre el tipo:

```python
TIPOS_DE_CUENTA = {
    "AHORRO": CuentaAhorro,
    "CORRIENTE": CuentaCorriente,
}
```

El diccionario asocia un texto a una **clase**, y la clase se usa como función
constructora. En la Iteración 5 se agrega `CuentaSueldo` y esto debe ser una
sola línea nueva.

### Operaciones

```python
depositar(cbu, monto) -> Cuenta
extraer(cbu, monto) -> Cuenta
transferir(cbu_origen, cbu_destino, monto) -> None
historial_de(cbu) -> list[Movimiento]
total_depositado() -> float
```

### `transferir` atómica

Es el método más delicado de la iteración. **O pasa entera o falla entera.**

Orden obligatorio:

1. buscar las dos cuentas (si alguna no existe → `CuentaInexistenteError`,
   nada se modificó);
2. verificar que no sean la misma (`TransferenciaInvalidaError`);
3. verificar que ambas estén activas (`CuentaInactivaError`);
4. **extraer del origen** — acá es donde puede fallar por fondos;
5. depositar en el destino;
6. registrar los movimientos como `"TRANSFERENCIA_SALIDA"` y
   `"TRANSFERENCIA_ENTRADA"`.

Si la extracción falla, el destino **no puede haber recibido nada**. Verificarlo
explícitamente en el escenario y en un test.

> Punto para discutir en grupo: el paso 5 también podría fallar (por ejemplo,
> si la cuenta destino tuviera un tope de saldo). ¿Qué habría que hacer
> entonces? Nombre de lo que están describiendo: *rollback*. Es el mismo
> problema que resuelven las transacciones de una base de datos.

### Métodos especiales

```python
__len__          # cantidad de cuentas activas
__contains__     # cbu in banco
__iter__         # for cuenta in banco  (recorre las activas)
__str__          # "Banco UTN - 12 cuentas activas - $1.250.000,00"
```

---

## 7. `main.py`: menú de consola

Es el **único** archivo del proyecto donde pueden aparecer `input()` y `print()`
(salvo los escenarios de demostración).

### Estructura

```python
def main():
    banco = Banco("Banco UTN")
    opciones = {
        "1": ("Abrir cuenta", opcion_abrir_cuenta),
        "2": ("Listar cuentas activas", opcion_listar),
        "3": ("Depositar", opcion_depositar),
        ...
        "0": ("Salir", None),
    }
```

El diccionario asocia cada opción con la **función que la resuelve**, sin
llamarla. Es el mismo patrón de diferir una operación que se practicó con
`lambda` en la Iteración 2.

Un `if/elif` de doce ramas para las opciones se considera incorrecto.

### Opciones mínimas

```text
1.  Abrir cuenta
2.  Listar cuentas activas
3.  Listar todas las cuentas (incluye cerradas)
4.  Buscar cuenta por CBU
5.  Depositar
6.  Extraer
7.  Transferir
8.  Ver resumen de una cuenta
9.  Ver historial de una cuenta
10. Liquidar intereses / cobrar mantenimiento
11. Cerrar cuenta
0.  Salir
```

### Manejo de errores

```python
try:
    accion(banco)
except BancoError as error:
    print(f"\n  [!] {type(error).__name__}: {error}")
```

Reglas:

- **no** capturar `Exception` a secas: un error de programación debe romper el
  programa y mostrar el *traceback*, no disfrazarse de error de negocio;
- el menú **no** valida reglas de negocio. No debe existir en `main.py` ningún
  `if monto <= 0` ni `if saldo < monto`: pide el dato, llama al banco y muestra
  lo que salga;
- convertir el texto del `input()` a número **sí** es responsabilidad del menú.

### Usar `else` y `finally` al menos una vez

```python
try:
    cuenta = banco.extraer(cbu, monto)
except BancoError as error:
    print(f"  [!] {error}")
else:
    print(f"  [OK] Nuevo saldo: ${cuenta.saldo:.2f}")
finally:
    input("\n  Enter para continuar...")
```

---

## 8. `pytest`

A partir de esta iteración las pruebas **se ejecutan**.

```bash
python -m pip install pytest
python -m pytest -q
```

`pytest.ini` en la raíz:

```ini
[pytest]
python_files = test.py test_*.py
testpaths = . tests
```

Se usa `python -m pytest` (con `-m`) para que la carpeta actual entre en el
`sys.path` y `from banco import ...` funcione.

Agregar al `.gitignore`:

```gitignore
.pytest_cache/
```

### Qué hay que entregar

1. `test.py` de la cátedra **pasando completo, sin modificarlo**;
2. al menos **12 tests propios** en `tests/`, escritos por el estudiante.

El detalle está en `TDD_ITERACION_04.md`.

---

## 9. Qué debe observarse al finalizar

- capturar `BancoError` alcanza para atrapar cualquier error del sistema;
- `except ValueError` sigue funcionando para los errores de validación;
- toda operación deja un movimiento con fecha y saldo posterior;
- un movimiento no se puede modificar después de creado;
- una transferencia fallida no modifica ninguna de las dos cuentas;
- la suma de los dos saldos se conserva en una transferencia exitosa;
- una cuenta cerrada no aparece en el listado activo, pero conserva su
  historial;
- los CBU los genera el sistema, no se repiten y pasan `validar_cbu`;
- `main.py` no contiene ninguna regla de negocio;
- `python -m pytest -q` termina sin fallos.

---

## 10. Decisiones de diseño para pensar

### 1. ¿Cuántas excepciones son demasiadas?

Una clase por cada mensaje posible es tan malo como una sola para todo.
Criterio: se justifica una clase nueva cuando **alguien la va a capturar por
separado**. Revisar la jerarquía y marcar cuáles aparecen efectivamente en un
`except`.

### 2. ¿Quién crea el `Movimiento`?

Lo crea la cuenta, dentro de `_registrar()`. ¿Podría un código externo agregar
un movimiento falso al historial? ¿Qué lo impide hoy?

### 3. ¿El `Banco` guarda las cuentas por CBU o por número?

Se eligió el CBU. ¿Qué pasaría si el usuario recuerda el número interno y no el
CBU? ¿Conviene un segundo índice? ¿Qué problema aparece al mantener dos
diccionarios sincronizados?

### 4. Baja lógica y listados

`listar_cuentas_activas()` filtra las cerradas. ¿Y `total_depositado()`?
¿Cuenta las cerradas? Justificar (pista: una cuenta cerrada tiene saldo `0`).

### 5. `__len__` de un banco

Se definió como "cantidad de cuentas activas". ¿Es evidente para quien lee
`len(banco)`? ¿Cuándo un método especial ayuda y cuándo confunde?

---

## 11. Forma de trabajo individual

Rama:

```text
iteracion-04/nombre-apellido
```

Orden sugerido:

1. mudar el código de la Iteración 3 a los módulos nuevos, sin cambiar lógica,
   y comprobar que el escenario sigue funcionando;
2. escribir `errores.py` y reemplazar las excepciones estándar;
3. escribir `Movimiento`;
4. agregar historial y baja lógica a `Cuenta`;
5. escribir `validar_cbu` y la generación de números;
6. escribir `Banco` con el ABM;
7. agregar `transferir` y probar el caso que falla;
8. escribir `main.py`;
9. configurar `pytest` y escribir los tests propios.

---

## 12. Commits sugeridos

```text
Reorganiza el proyecto en modulos
Agrega jerarquia de errores del dominio
Reemplaza excepciones estandar por errores propios
Implementa clase Movimiento
Agrega historial de movimientos a Cuenta
Implementa baja logica de cuentas
Agrega validacion y generacion de CBU
Implementa clase Banco con ABM de cuentas
Implementa transferencia atomica
Agrega menu de consola en main.py
Configura pytest y pytest.ini
Agrega tests de banco y transferencias
```

---

## 13. Integración grupal

Rama:

```text
integracion/iteracion-04
```

En la comparación el grupo debe discutir:

- qué tan profunda quedó la jerarquía de errores en cada solución;
- en qué orden resolvió cada uno la transferencia;
- cómo resolvió cada uno la fábrica de cuentas;
- qué tests propios conviene conservar (la suite integrada debe ser la unión de
  los mejores, no la de un solo integrante).

**Condición de la entrega:** `python -m pytest -q` debe pasar en la rama
`integracion/iteracion-04` antes de abrir el Pull Request hacia `main`.

---

## Criterio central

Las dos preguntas de esta iteración:

> ¿El código que llama a una operación puede reaccionar distinto según **qué**
> salió mal, sin leer el texto del mensaje de error?

> ¿Podría reemplazarse la interfaz entera sin tocar una línea de lógica
> bancaria?
