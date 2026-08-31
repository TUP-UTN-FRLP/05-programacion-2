# Proyecto Integrador Banco — Iteración 2

## Introducción

En la Iteración 1 construimos una `Cuenta` mínima y, deliberadamente, permitimos
situaciones incorrectas: depósitos negativos, extracciones sin fondos, cuentas
con datos vacíos y modificación directa del saldo desde afuera.

En esta segunda etapa vamos a resolver esas limitaciones con dos herramientas
que ya trabajamos en teoría:

- **encapsulamiento** (atributos internos + `@property` de solo lectura);
- **validación** (funciones que verifican los datos y cortan con una excepción
  cuando el contrato no se cumple).

El sistema sigue siendo pequeño. No estamos construyendo todavía el CRUD del
banco. El objetivo es que las entidades **no puedan nacer con un estado
inválido** y que su estado no se pueda romper desde afuera.

---

## Qué cambia respecto de la Iteración 1

Leer esto antes de empezar. La Iteración 2 **modifica** cosas de la 1:

| Tema | Iteración 1 | Iteración 2 |
| --- | --- | --- |
| Entidades | solo `Cuenta` | `Persona` y `Cuenta` |
| Titular | un `str` cualquiera | un objeto `Persona` (si no, `TypeError`) |
| Número de cuenta | texto libre (`"001-234"`) | `str` de **exactamente 14 dígitos** |
| `depositar` / `extraer` | sin validar nada | validan el monto; `extraer` valida saldo |
| Atributos | públicos (`cuenta.saldo = 9999` permitido) | encapsulados + `@property` de solo lectura |
| Datos inválidos | permitidos | rechazados con `ValueError` / `TypeError` |
| Archivo | un único `banco.py` | `banco.py` + `validaciones.py` |
| Escenario de prueba | código suelto al final del archivo | dentro de un bloque `if __name__ == "__main__":` |
| Repositorio | sin `.gitignore` | con `.gitignore` (no versionar `__pycache__/`, etc.) |

Los datos de prueba de la Iteración 1 (números como `"001-234"`) **ya no son
válidos**: hay que adaptarlos al formato nuevo.

---

## Objetivo de la Iteración 2

Al finalizar, el programa deberá modelar dos entidades:

- `Persona`;
- `Cuenta`.

La relación entre ellas será:

```text
Persona
   │
   │ es titular de
   ▼
Cuenta
```

Una `Cuenta` **tiene un titular**, que debe ser un objeto `Persona`. Esto es
**composición**: la cuenta guarda una referencia a un objeto de otra clase.

---

## Conceptos que se trabajan

- clases y objetos;
- `__init__`;
- atributos encapsulados con doble guion bajo (`__atributo`) y *name mangling*;
- `@property` para lectura controlada (sin setters);
- composición entre objetos (`Cuenta` tiene una `Persona`);
- validaciones;
- funciones auxiliares de validación en un módulo aparte;
- excepciones estándar (`ValueError` y `TypeError`);
- módulos e importaciones;
- el bloque `if __name__ == "__main__":` para separar el código de escenario;
- `lambda` para diferir la ejecución de cada caso inválido del escenario;
- `__str__` para representaciones legibles;
- `.gitignore` para no versionar archivos generados.

> **Sobre `test.py` y `pytest`:** el repositorio debería incluir un archivo
> `test.py`, y más adelante se trabaja con `pytest`. En esta iteración **no se
> usan ni se crean**: se mencionan para que se sepa que existen, pero la
> verificación se hace igual que en la Iteración 1, ejecutando el escenario de
> `banco.py`. `pytest` se incorpora formalmente en la Iteración 4. No hace falta
> instalarlo ahora.

Hay una guía de acompañamiento para los grupos en `INICIO_ITERACION_02.md`
(explica el `if __name__ == "__main__":`, su relación con el *namespace* y el
*name mangling*, y para qué sirve el `.gitignore`).

---

## Importante: qué NO buscamos todavía

En esta iteración **no** se debe implementar:

- registro de movimientos ni historial de la cuenta;
- fechas (`datetime`);
- herencia y polimorfismo;
- múltiples tipos de cuenta (ahorro / corriente);
- transferencias entre cuentas;
- persistencia en archivos o base de datos;
- CRUD completo de personas o cuentas;
- menú interactivo o `input()`;
- Django, Flask o FastAPI;
- interfaz gráfica o frontend;
- excepciones personalizadas.

> Los **movimientos, el historial y las fechas** se incorporan más adelante en
> el proyecto. No agregarlos ahora.

El objetivo es concentrarse en que las entidades queden bien construidas y
protegidas.

---

## Organización de archivos

```text
banco.py          # clases Persona y Cuenta + escenario en if __name__ == "__main__"
validaciones.py   # funciones de validación reutilizables
test.py           # suite de la cátedra; se lee como referencia, no se ejecuta en esta iteración
.gitignore        # archivos que NO se versionan
```

`banco.py` mantiene el nombre pedido en la Iteración 1. Las validaciones
reutilizables van en `validaciones.py`. Las clases **no** deben pedir datos con
`input()` ni imprimir mensajes para decidir si un dato es válido: si un dato es
inválido, se corta con una excepción.

El escenario de prueba se coloca dentro de un bloque
`if __name__ == "__main__":` al final de `banco.py`, para que al importar el
módulo desde otro archivo ese código **no** se ejecute. La explicación completa
está en `INICIO_ITERACION_02.md`.

---

## 1. Clase `Persona`

Archivo: `banco.py`

Representa a una persona titular de una cuenta.

### Atributos de la persona

Encapsulados (doble guion bajo):

```text
__nombre
__apellido
__dni
```

### Constructor de `Persona`

```python
Persona(nombre, apellido, dni)
```

### Reglas de validación

#### Nombre y apellido

- deben ser `str` (si no, `TypeError`);
- no pueden quedar vacíos después de `strip()` (si no, `ValueError`);
- solo se admiten **letras** (incluidas tildes y `ñ`), **espacios**, **guion**
  (`-`) y **apóstrofo** (`'`); cualquier otro carácter → `ValueError`;
- los espacios internos repetidos se reducen a uno;
- se almacenan normalizados con formato de nombre (`str.title()`).

Ejemplos:

```text
"  ana   maría "   ->  "Ana María"
"de   la   cruz"   ->  "De La Cruz"
"o'brien-smith"    ->  "O'Brien-Smith"
```

> Nota: `str.title()` pone en mayúscula la primera letra de cada palabra,
> incluidas las partículas (`"De La Cruz"`). Para esta iteración lo aceptamos
> así; es una simplificación conocida.

#### DNI

- debe recibirse como `str` (si se pasa un número → `TypeError`);
- solo dígitos `0-9`;
- 7 u 8 dígitos;
- se guarda tal cual (con los ceros a la izquierda si los tiene).

El DNI es un identificador, no un número para hacer cálculos.

### Propiedades de lectura de `Persona`

```text
nombre
apellido
dni
nombre_completo   ->  "Apellido, Nombre"
```

No se implementan setters. Intentar `persona.nombre = "Otro"` debe fallar con
`AttributeError`.

### Representación de `Persona` con `__str__`

Formato libre pero legible. Ejemplo:

```text
Pérez, Ana (DNI 12345678)
```

---

## 2. Clase `Cuenta`

Archivo: `banco.py`

### Atributos de la cuenta

Encapsulados:

```text
__numero
__titular
__saldo
```

### Constructor de `Cuenta`

```python
Cuenta(numero, titular, saldo_inicial=0)
```

### Número de cuenta

- debe ser un `str` (si no, `TypeError`);
- exactamente **14 dígitos**, sin letras, espacios ni separadores
  (si no, `ValueError`).

Ejemplo válido:

```text
12345678901234
```

### Titular

- debe ser una instancia de `Persona`;
- si se pasa un `str`, `None` o cualquier otro tipo → `TypeError`.

Relación: **`Cuenta` tiene una `Persona`** (composición).

### Saldo inicial

- debe ser `int` o `float` (`bool` no cuenta como número → `TypeError`);
- no puede ser negativo (`ValueError`);
- valor por defecto `0`.

El saldo es de **solo lectura** desde afuera. `cuenta.saldo = 9999` debe fallar
con `AttributeError`.

### Propiedades de lectura de `Cuenta`

```text
numero
titular
saldo
```

No se implementan setters.

### Representación de `Cuenta` con `__str__`

Ejemplo (mismo espíritu que en la Iteración 1):

```text
Cuenta N° 12345678901234 - Pérez, Ana - Saldo: $1300.00
```

---

## 3. Operaciones de la cuenta

Se conservan `depositar()` y `extraer()` de la Iteración 1, pero ahora
**protegen el estado**.

### `depositar(monto)`

1. validar que `monto` sea `int`/`float` y `> 0` (si no, `TypeError` o
   `ValueError`);
2. aumentar el saldo.

### `extraer(monto)`

1. validar que `monto` sea `int`/`float` y `> 0`;
2. comprobar que haya saldo suficiente; si `monto > saldo`, cortar con
   `ValueError` **sin modificar el saldo**;
3. disminuir el saldo.

En esta iteración el saldo ya **no** puede quedar negativo.

---

## 4. Archivo `validaciones.py`

Las validaciones que no necesitan `self` van separadas de las clases.

Funciones públicas esperadas (nombres y contrato usados por `test.py`):

```python
validar_nombre(valor)
validar_dni(valor)
validar_numero_cuenta(valor)
validar_saldo_inicial(valor)
validar_monto(valor)
```

Una función de validación:

- recibe un valor;
- comprueba una regla;
- devuelve el valor **normalizado** cuando corresponde (p. ej. `validar_nombre`
  devuelve el nombre con formato; `validar_dni` devuelve el mismo `str`);
- lanza `TypeError` si el **tipo** no corresponde;
- lanza `ValueError` si el tipo es correcto pero el **valor** no cumple la regla;
- no usa `input()` ni `print()`;
- no depende de una instancia de `Persona` ni `Cuenta`.

Las clases de `banco.py` deben **usar** estas funciones, no repetir la lógica.

---

## 5. `banco.py`: escenario obligatorio

Dentro de `if __name__ == "__main__":`, el archivo debe:

1. crear una `Persona`;
2. crear una `Cuenta` cuyo titular sea esa persona (saldo inicial `0`);
3. realizar varias operaciones **válidas** (depósitos y extracciones);
4. imprimir los datos del titular usando sus propiedades;
5. imprimir la cuenta (`print(cuenta)`);
6. mostrar, capturando la excepción con `try/except`, que ahora **fallan**:
   - `cuenta.depositar(-500)`   → `ValueError`
   - `cuenta.extraer(100000)`   → `ValueError`
   - `Cuenta("12345678901234", "Ana Pérez")` → `TypeError`
   - `Cuenta("12345678901234", titular, -1000)` → `ValueError`
   - `cuenta.saldo = 99999999`  → `AttributeError`

No hace falta `input()`. Los datos van escritos directamente en `banco.py`.

### Refuerzo: `lambda` para diferir cada caso inválido

Los cinco casos que deben fallar conviene recorrerlos con un `for` sobre una
lista de pares `(descripción, acción)`, y capturar la excepción una sola vez:

```python
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
        print(f"  [FALLO] {descripcion}: no lanzo excepcion")
    except (ValueError, TypeError, AttributeError) as error:
        print(f"  [OK] {descripcion}: {type(error).__name__} - {error}")
```

**Qué es.** `lambda` crea una **función anónima** de una sola expresión
(`lambda parámetros: expresión`). Acá se usa **sin parámetros**: `lambda:
cuenta.depositar(-500)` no deposita nada; devuelve una función que hará esa
llamada *cuando se la invoque*.

**Por qué se usa.** Se necesita guardar en la lista la **operación**, no su
resultado. Si se escribiera `("...", cuenta.depositar(-500))`, esa llamada se
ejecutaría al **construir la lista** —antes del `for`— y, como lanza
`ValueError`, el programa se cortaría ahí. Envuelta en `lambda:`, la ejecución
se **difiere** hasta el `try`.

**Cómo se usa.** El `for` desarma cada tupla en `descripcion` y `accion`;
`accion()` —con los paréntesis— dispara la llamada dentro del `try`. Así hay
**un solo** `try/except` en lugar de cinco casi iguales, y sumar o quitar un
caso es una línea. Es el mismo patrón —guardar una operación para ejecutarla
más tarde— que reaparece en la **Iteración 4**, cuando cada opción del menú se
asocia a una función.

> Este bloque `if __name__ == "__main__":` es provisorio: en la **Iteración 4**
> lo vamos a reemplazar por un menú de consola para el CRUD de `Persona` y
> `Cuenta`. Por eso conviene que el escenario quede prolijo y aislado del resto
> del archivo. Ver `INICIO_ITERACION_02.md`.

---

## 6. `.gitignore`

El repositorio debe incluir un archivo `.gitignore` en la raíz **antes del
primer commit** de la iteración, para no versionar archivos que Python o las
herramientas generan solos:

```gitignore
__pycache__/
*.py[cod]
.venv/
venv/
.idea/
.vscode/
```

Qué es cada cosa y por qué molesta tenerlo en el repo está explicado en
`INICIO_ITERACION_02.md`. Si en la Iteración 1 quedó algún `__pycache__/`
commiteado, sacarlo con `git rm -r --cached __pycache__`.

> En la Iteración 4, al empezar a usar `pytest`, se agrega también la línea
> `.pytest_cache/`. Ahora no hace falta porque no se ejecuta `pytest`.

---

## 7. Qué debe observarse al finalizar

- no se puede crear una `Persona` con DNI inválido;
- no se puede crear una `Cuenta` sin un objeto `Persona` como titular;
- no se puede crear una cuenta con saldo inicial negativo;
- el saldo no se puede asignar directamente desde afuera;
- un depósito o una extracción con monto `<= 0` se rechaza;
- una extracción mayor al saldo se rechaza y el saldo no cambia;
- la relación `Cuenta` → `Persona` puede explicarse como composición.

---

## 8. Sobre `test.py` (no se usa en esta iteración)

La cátedra entrega **un** archivo `test.py` con una suite de `pytest`. Describe,
en forma de código, el comportamiento esperado: constructores, properties de
solo lectura, normalización, validaciones, la relación `Cuenta` → `Persona` y
las operaciones `depositar()` / `extraer()`.

En la Iteración 2 **no se ejecuta** `pytest`. El archivo se incluye para poder
leerlo como referencia del contrato y para que quede en el repositorio; el
trabajo con `pytest` (instalación, ejecución, ciclo TDD, `pytest.ini`) se
incorpora en la Iteración 4, cuando el código deja de cambiar tanto.

La verificación de esta iteración se hace como en la Iteración 1: ejecutando el
escenario de `banco.py` (sección 5) y comprobando que las operaciones válidas
funcionan y que las inválidas se rechazan con la excepción correcta.

---

## 9. Forma de trabajo individual

Cada integrante resuelve la iteración completa en su propia rama:

```text
iteracion-02/nombre-apellido
```

Cada estudiante deberá:

- implementar personalmente `Persona`, `Cuenta` y las validaciones;
- completar el escenario de `banco.py` y ejecutarlo para comprobar el comportamiento;
- hacer commits identificables durante el proceso;
- publicar su rama;
- abrir un Pull Request hacia la rama de integración del grupo.

---

## 10. Commits sugeridos

```text
Agrega validaciones base en validaciones.py
Implementa clase Persona con properties de solo lectura
Implementa encapsulamiento de Cuenta
Valida depositar y extraer
Agrega escenario en banco.py
Ajusta validaciones y normalizacion
Agrega .gitignore
```

Evitar: `cambios`, `cosas`, `prueba`, `final`.

---

## 11. Integración grupal

Una vez publicadas las soluciones individuales, el grupo construye una versión
consensuada en:

```text
integracion/iteracion-02
```

El **líder de la semana** revisa los Pull Requests, coordina la integración y
abre el Pull Request final hacia `main`, que revisa la cátedra.

---

## 12. Entrega de la Iteración 2

La versión integrada deberá contener:

```text
banco.py
validaciones.py
test.py           # tal como lo entregó la cátedra, sin modificar
.gitignore
```

Y deberá demostrar:

- encapsulamiento con properties de solo lectura;
- validaciones que impiden estados inválidos;
- composición: una `Cuenta` con un titular `Persona`;
- `depositar()` y `extraer()` que protegen el saldo;
- el escenario de `banco.py` mostrando que los casos inválidos se rechazan;
- código que todos los integrantes puedan explicar.

---

## Criterio central

La pregunta ya no es solo:

> ¿El programa funciona?

Ahora también:

> ¿Los objetos protegen su propio estado y representan correctamente la relación
> entre `Cuenta` y `Persona`?
