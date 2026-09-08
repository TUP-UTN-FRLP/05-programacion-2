# Contrato de comportamiento — Iteración 3 — Herencia y especialización

> **Desde la Iteración 3 `test.py` se ejecuta con `pytest`.** Este documento y
> `test.py` describen el comportamiento esperado de las dos jerarquías; la suite
> se corre (`python -m pytest -q`) y pasarla completa es condición de entrega.
> Herramienta y puesta en marcha: `GUIA_TESTS_ITERACION_03.md`.

## Propósito

`test.py` es el **contrato técnico** de la iteración: fija los nombres y el
comportamiento observable. Si la implementación no respeta esos nombres, en la
Iteración 4 la suite no va a poder importarla.

Novedad respecto de la Iteración 2: además de casos sueltos, este contrato
incluye **invariantes** (propiedades que deben valer siempre, no solo en un
caso) y un **contrato de subclase** que toda clase derivada debe cumplir.

---

## Estructura del proyecto

```text
banco.py          # Persona, PersonaFisica, PersonaJuridica,
                  # Cuenta, CuentaAhorro, CuentaCorriente
validaciones.py
test.py           # esta suite; se ejecuta con pytest, no se modifica
test_propios.py   # pruebas propias del estudiante (prefijo test_)
pytest.ini
.gitignore        # incluye .pytest_cache/ y __pycache__/
```

`test.py` importa así:

```python
from banco import (
    Cuenta,
    CuentaAhorro,
    CuentaCorriente,
    Persona,
    PersonaFisica,
    PersonaJuridica,
)
from validaciones import (
    validar_cuit,
    validar_dni,
    validar_edad,
    validar_limite,
    validar_monto,
    validar_nombre,
    validar_numero_cuenta,
    validar_razon_social,
    validar_saldo_inicial,
    validar_tasa,
)
```

Los nombres de módulos, clases, funciones y properties deben ser exactamente
esos.

---

## Contrato de `validaciones.py`

| Función | Devuelve | `TypeError` | `ValueError` |
| --- | --- | --- | --- |
| `validar_nombre(v)` | `str` con `title()` | no es `str` | vacío o caracteres no permitidos |
| `validar_dni(v)` | `str` tal cual | no es `str` | no son 7 u 8 dígitos |
| `validar_numero_cuenta(v)` | `str` tal cual | no es `str` | no son 14 dígitos |
| `validar_saldo_inicial(v)` | `int`/`float` | no numérico, o `bool` | negativo |
| `validar_monto(v)` | `int`/`float` | no numérico, o `bool` | `<= 0` |
| `validar_razon_social(v)` | `str` normalizado | no es `str` | vacío o caracteres no permitidos |
| `validar_cuit(v)` | `str` de 11 dígitos | no es `str` | no son 11 dígitos, o el verificador no cierra |
| `validar_edad(v)` | `int` | no es `int`, o es `bool`, o es `float` | fuera de `[18, 120]` |
| `validar_tasa(v)` | `int`/`float` | no numérico, o `bool` | fuera de `[0, 1]` |
| `validar_limite(v)` | `int`/`float` | no numérico, o `bool` | negativo |

### Cómo se construye el CUIL / CUIT

El CUIT (empresas) y el CUIL (personas físicas) se arman igual: 11 dígitos,
`XX-XXXXXXXX-X`. Los 10 primeros son datos (prefijo de tipo + cuerpo) y el
dígito 11 se **calcula** por módulo 11.

```text
1. tomar los 10 primeros dígitos;
2. multiplicarlos, en orden, por los pesos  5 4 3 2 7 6 5 4 3 2;
3. suma = Σ(dígito_i · peso_i);
4. resto = suma % 11;
5. verificador = 11 - resto;
      resto == 0   ->  verificador = 11 - 0  = 11  ->  se usa 0
      resto == 1   ->  verificador = 11 - 1  = 10  ->  CUIT inválido
      resto 2..10  ->  verificador = 11 - resto     (un dígito 1..9)
6. el verificador calculado debe coincidir con el dígito 11 recibido.
```

Ejemplo completo con `30712345671`:

```text
dígitos    3   0   7   1   2   3   4   5   6   7
pesos      5   4   3   2   7   6   5   4   3   2
producto  15   0  21   2  14  18  20  20  18  14   ->  suma = 142

142 % 11 = 10        verificador = 11 - 10 = 1     ->  coincide  (CUIT válido)
```

El mismo número con el dígito 11 en `0` (`30712345670`) no cierra: `ValueError`.

`validar_cuit` no verifica el prefijo (`20/23/24/27` física, `30/33/34`
jurídica): solo formato de 11 dígitos y dígito verificador.

### Casos puntuales de `validar_cuit`

| Entrada | Esperado |
| --- | --- |
| `"30712345671"` | devuelve `"30712345671"` |
| `"20123456786"` | devuelve `"20123456786"` |
| `"27234567891"` | devuelve `"27234567891"` |
| `"30712345670"` | `ValueError` (verificador incorrecto) |
| `"3071234567"` | `ValueError` (10 dígitos) |
| `"307123456712"` | `ValueError` (12 dígitos) |
| `"3071234567a"` | `ValueError` (tiene una letra) |
| `"30-71234567-1"` | `ValueError` (tiene guiones) |
| `30712345671` | `TypeError` (es `int`) |
| `""` | `ValueError` |

### Casos puntuales de `validar_edad`

| Entrada | Esperado |
| --- | --- |
| `18`, `65`, `120` | devuelve el `int` |
| `17`, `0`, `-5`, `121` | `ValueError` |
| `"30"` | `TypeError` |
| `30.0` | `TypeError` |
| `True` | `TypeError` |

---

## Contrato de `Persona` (clase base)

| Caso | Esperado |
| --- | --- |
| `Persona("Ana")` | se puede instanciar (limitación conocida de esta iteración) |
| `persona.nombre` | normalizado con `title()` |
| `persona.identificacion` | `"SIN IDENTIFICACION"` |
| `persona.nombre = "Otro"` | `AttributeError` |
| `Persona(123)` | `TypeError` |
| `Persona("   ")` | `ValueError` |

---

## Contrato de `PersonaFisica`

```python
PersonaFisica(nombre, apellido, dni, edad)
```

| Caso | Esperado |
| --- | --- |
| `issubclass(PersonaFisica, Persona)` | `True` |
| `isinstance(fisica, Persona)` | `True` |
| `fisica.nombre` / `fisica.apellido` | normalizados con `title()` |
| `fisica.nombre_completo` | `"Apellido, Nombre"` |
| `fisica.dni` | el `str` recibido, tal cual |
| `fisica.edad` | el `int` recibido |
| `fisica.identificacion` | contiene `"DNI"` y el número |
| `PersonaFisica("Ana", "Perez", 12345678, 30)` | `TypeError` |
| `PersonaFisica("Ana", "Perez", "123", 30)` | `ValueError` |
| `PersonaFisica("Ana", "Perez", "12345678", 17)` | `ValueError` |
| `PersonaFisica("", "Perez", "12345678", 30)` | `ValueError` |
| `fisica.dni = "99999999"` | `AttributeError` |
| `fisica.edad = 99` | `AttributeError` |

**Invariante de reutilización:** las reglas de `nombre` de la Iteración 2 deben
seguir valiendo sin que `PersonaFisica` las reimplemente. Si en el código de la
subclase aparece la normalización del nombre, la herencia no está cumpliendo su
función.

---

## Contrato de `PersonaJuridica`

```python
PersonaJuridica(razon_social, cuit)
```

| Caso | Esperado |
| --- | --- |
| `issubclass(PersonaJuridica, Persona)` | `True` |
| `juridica.razon_social` | igual a `juridica.nombre` |
| `"Distribuidora S.A."` | aceptada (tiene puntos) |
| `"3M Argentina S.R.L."` | aceptada (tiene dígitos) |
| `"Perez & Cia., S.R.L."` | aceptada |
| `""` / `"   "` | `ValueError` |
| `PersonaJuridica(123, "30712345671")` | `TypeError` |
| `juridica.cuit` | los 11 dígitos, sin guiones |
| `juridica.identificacion` | contiene `"CUIT"` y el número con guiones `30-71234567-1` |
| `PersonaJuridica("Distribuidora S.A.", "30712345670")` | `ValueError` |
| `juridica.cuit = "20123456786"` | `AttributeError` |
| `hasattr(juridica, "dni")` | `False` |

---

## Contrato de `Cuenta` (clase base)

Se conserva íntegro el contrato de la Iteración 2, con dos agregados.

| Caso | Esperado |
| --- | --- |
| `Cuenta.TIPO` | `"Cuenta"`, accesible sin instanciar |
| `numero` no `str` / no 14 dígitos | `TypeError` / `ValueError` |
| `titular` que no es `Persona` | `TypeError` |
| `titular` `PersonaFisica` o `PersonaJuridica` | aceptado |
| `saldo_inicial` negativo / `bool` | `ValueError` / `TypeError` |
| `cuenta.saldo = 9999` | `AttributeError` |
| `depositar(monto)` válido | el saldo aumenta exactamente en `monto` |
| `depositar(0)` / `depositar(-1)` | `ValueError`, saldo sin cambios |
| `extraer(monto)` en la base | permite dejar el saldo negativo (no hay regla) |
| `cuenta.resumen()` | `str` que contiene el número, el titular y el saldo |
| `cuenta.resumen()` | contiene `TIPO` |

---

## Contrato de `CuentaAhorro`

```python
CuentaAhorro(numero, titular, saldo_inicial=0, tasa_interes=0.01)
```

| Caso | Esperado |
| --- | --- |
| `issubclass(CuentaAhorro, Cuenta)` | `True` |
| `CuentaAhorro.TIPO` | `"Caja de Ahorro"` |
| `CuentaAhorro.TASA_POR_DEFECTO` | accesible sin instanciar |
| `tasa_interes` omitida | toma el valor por defecto |
| `tasa_interes` fuera de `[0, 1]` | `ValueError` |
| `tasa_interes` `str` o `bool` | `TypeError` |
| `cuenta.tasa_interes = 0.5` | `AttributeError` |
| saldo 1000, `extraer(1000)` | permitido, saldo `0` |
| saldo 1000, `extraer(1000.01)` | `ValueError`, saldo sin cambios |
| saldo 0, `extraer(1)` | `ValueError` |
| `extraer(-100)` | `ValueError` (regla heredada) |
| `extraer("100")` | `TypeError` (regla heredada) |
| saldo 1000, tasa 0.01, `liquidar_interes()` | devuelve `10`, saldo `1010` |
| saldo 0, `liquidar_interes()` | devuelve `0`, saldo `0` |
| `resumen()` | además del texto base, incluye la tasa |

**Invariante:** después de cualquier secuencia de operaciones válidas,
`ahorro.saldo >= 0`.

---

## Contrato de `CuentaCorriente`

```python
CuentaCorriente(numero, titular, saldo_inicial=0, limite_descubierto=0)
```

| Caso | Esperado |
| --- | --- |
| `issubclass(CuentaCorriente, Cuenta)` | `True` |
| `CuentaCorriente.TIPO` | `"Cuenta Corriente"` |
| `CuentaCorriente.COSTO_MANTENIMIENTO` | accesible sin instanciar |
| `limite_descubierto` omitido | `0` |
| `limite_descubierto` negativo | `ValueError` |
| `limite_descubierto` `bool` o `str` | `TypeError` |
| `cuenta.limite_descubierto = 5000` | `AttributeError` |
| `saldo_disponible` | `saldo + limite_descubierto`, recalculado tras cada operación |
| saldo 1000, límite 5000, `extraer(6000)` | permitido, saldo `-5000` |
| saldo 1000, límite 5000, `extraer(6000.01)` | `ValueError`, saldo sin cambios |
| saldo 1000, límite 0, `extraer(1001)` | `ValueError` |
| `cobrar_mantenimiento()` | descuenta `COSTO_MANTENIMIENTO`; puede dejar saldo negativo |
| `resumen()` | además del texto base, incluye límite y disponible |

**Invariante:** después de cualquier secuencia de extracciones válidas,
`corriente.saldo >= -corriente.limite_descubierto`. El cobro de mantenimiento
es la única operación autorizada a superar ese límite.

---

## Contrato de polimorfismo

Estos casos son los que verifican que la jerarquía sirve para algo:

| Caso | Esperado |
| --- | --- |
| lista `[ahorro, corriente]`, llamar `resumen()` en un `for` | cada elemento devuelve un texto distinto |
| lista `[fisica, juridica]`, leer `identificacion` en un `for` | cada elemento devuelve un texto distinto |
| `resumen()` de una subclase | contiene el texto de `Cuenta.resumen()` (se usó `super()`) |
| `depositar()` | es el mismo método heredado en ambas subclases |
| ninguna subclase | define `depositar()` |

El último caso se verifica así:

```python
assert "depositar" not in CuentaAhorro.__dict__
assert "depositar" not in CuentaCorriente.__dict__
```

`__dict__` de una clase contiene solo lo definido **en esa** clase, no lo
heredado. Es la forma directa de comprobar que no se duplicó código.

---

## Contrato de subclase

Cualquier clase que herede de `Cuenta` —hoy dos, en la Iteración 5 tres— debe
cumplir:

1. su `__init__` llama a `super().__init__(numero, titular, saldo_inicial)` con
   los mismos tres primeros parámetros y en el mismo orden;
2. no exige parámetros obligatorios adicionales en `extraer()` ni en
   `depositar()`;
3. no relaja las validaciones de la clase base (lo que la base rechaza, la
   subclase también);
4. redefine `TIPO`;
5. si sobrescribe `resumen()`, incluye el resultado de `super().resumen()`.

Los puntos 1 a 3 son la versión práctica del **principio de sustitución**: una
lista de `Cuenta` debe poder recorrerse llamando a los mismos métodos sin
preguntar de qué clase es cada elemento. En la Iteración 5 esto se verifica con
`assert` explícitos.

---

## Qué NO verifica este contrato

- el formato exacto de `__str__` y `resumen()` (solo qué datos debe contener);
- la salida por pantalla del escenario de `banco.py`;
- el redondeo del interés;
- la precisión de los `float` (`0.1 + 0.2` no da `0.3`; se acepta en este
  proyecto).

Cumplir el contrato es condición **necesaria pero no suficiente**: la iteración
se completa con el escenario de `banco.py` y la revisión grupal.

---

## Orden sugerido para trabajar

1. Agregar las validaciones nuevas a `validaciones.py`, empezando por
   `validar_cuit` (es la única con cálculo).
2. Refactorizar `Persona` como clase base y mover el `dni`.
3. Escribir `PersonaFisica` y comprobar que no repite validaciones.
4. Escribir `PersonaJuridica`.
5. Agregar `TIPO` y `resumen()` a `Cuenta`.
6. Escribir `CuentaAhorro` y ejecutar el escenario parcial.
7. Escribir `CuentaCorriente` y comprobar el bucle polimórfico.
8. Completar el escenario y los casos que deben fallar.
