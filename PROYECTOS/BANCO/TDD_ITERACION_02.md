# Contrato de comportamiento — Iteración 2 — Entidades, encapsulamiento y validación

> **`pytest` no se usa en la Iteración 2.** Este documento y el archivo `test.py`
> describen, en detalle, el comportamiento que deben tener `Persona`, `Cuenta` y
> `validaciones.py`. En esta iteración se usan solo como **referencia de
> lectura** y como lista de casos para comprobar a mano dentro del escenario de
> `banco.py`. La ejecución de `test.py` con `pytest` (instalación, ciclo TDD,
> `pytest.ini`) se incorpora en la **Iteración 4**.

## Propósito

`test.py` es un **contrato técnico parcial** para la Iteración 2.

No contiene la solución y no verifica todo el comportamiento. Su objetivo es
documentar el comportamiento esperado de `Persona` y `Cuenta` y describir:

- las funciones de `validaciones.py`;
- los constructores de `Persona` y `Cuenta`;
- la normalización de datos;
- las properties de solo lectura (sin setters);
- la relación `Cuenta` → `Persona` (composición);
- las operaciones `depositar()` y `extraer()`.

Lo que **no** verifica: el formato exacto de `__str__` y la salida del escenario
de `banco.py`. Eso queda a cargo del estudiante.

---

## Estructura del proyecto

```text
banco.py          # clases Persona y Cuenta
validaciones.py   # funciones de validación
test.py           # esta suite (referencia; se ejecuta a partir de la Iteración 4)
.gitignore        # archivos que no se versionan
```

`test.py` importa así:

```python
from banco import Cuenta, Persona
from validaciones import (
    validar_dni,
    validar_monto,
    validar_nombre,
    validar_numero_cuenta,
    validar_saldo_inicial,
)
```

Por lo tanto, los nombres de módulos, clases y funciones deben ser exactamente
esos.

---

## Cómo se usa en la Iteración 2

No se ejecuta. Se abre `test.py` y se lee cada función de test como un caso
concreto: qué entrada recibe la clase o la validación y qué se espera (un valor
normalizado o una excepción). Cada uno de esos casos se puede reproducir a mano
dentro del escenario de `banco.py` para comprobar el comportamiento.

## Cómo se ejecutará (Iteración 4)

A partir de la Iteración 4, con `pytest` ya incorporado:

```bash
python -m pip install pytest      # una sola vez
python -m pytest -q               # con el pytest.ini en la raíz
```

`python -m pytest` (con `-m`) agrega la carpeta actual al `sys.path`, así
`from banco import ...` funciona. El `pytest.ini` hace que `pytest` descubra
`test.py` además de `test_*.py`.

---

## Contrato de `validaciones.py`

```python
validar_nombre(valor)          # -> str normalizado con title(); TypeError / ValueError
validar_dni(valor)             # -> str de 7 u 8 dígitos, tal cual; TypeError / ValueError
validar_numero_cuenta(valor)   # -> str de 14 dígitos, tal cual; TypeError / ValueError
validar_saldo_inicial(valor)   # -> int/float >= 0; TypeError / ValueError
validar_monto(valor)           # -> int/float > 0; TypeError / ValueError
```

Criterio de errores:

- `TypeError` cuando el **tipo** recibido no corresponde (incluye `bool`, que no
  cuenta como número, y `None`);
- `ValueError` cuando el tipo es correcto pero el **valor** no cumple la regla.

No se usan excepciones personalizadas en esta iteración.

---

## Contrato de `Persona`

```python
Persona(nombre, apellido, dni)
```

Properties (solo lectura): `nombre`, `apellido`, `dni`, `nombre_completo`
(`"Apellido, Nombre"`).

`nombre` y `apellido` se normalizan: `strip()`, espacios internos colapsados a
uno, `str.title()`. Se admiten letras (con tildes y `ñ`), espacios, `-` y `'`.

`dni` se recibe como `str`; si se pasa un `int` → `TypeError`.

---

## Contrato de `Cuenta`

```python
Cuenta(numero, titular, saldo_inicial=0)
```

Properties (solo lectura): `numero`, `titular`, `saldo`.

- `numero`: `str` de exactamente 14 dígitos (`TypeError` si no es `str`,
  `ValueError` si el formato no cierra);
- `titular`: instancia de `Persona` (`str`, `None` u otro tipo → `TypeError`);
- `saldo_inicial`: numérico y no negativo (`bool` → `TypeError`, negativo →
  `ValueError`).

Operaciones:

- `depositar(monto)`: valida el monto (`> 0`) y aumenta el saldo;
- `extraer(monto)`: valida el monto (`> 0`), verifica saldo suficiente
  (`ValueError` si no alcanza, **sin** tocar el saldo) y lo disminuye.

No hay setters. `cuenta.saldo = 9999` debe lanzar `AttributeError`.

---

## Orden sugerido para trabajar

1. Leer los casos de `test.py` correspondientes a `validaciones.py`.
2. Implementar `validaciones.py`, una función por vez.
3. Implementar `Persona` usando las validaciones ya escritas.
4. Implementar la construcción y el encapsulamiento de `Cuenta`.
5. Implementar `depositar()` y `extraer()`.
6. Completar el escenario de `banco.py` (`if __name__ == "__main__":`) y
   ejecutarlo para comprobar el comportamiento.

---

## Qué NO prueba `test.py`

- el formato exacto de `__str__`;
- la salida por pantalla del escenario de `banco.py`;
- secuencias largas de operaciones combinadas.

Cumplir con todos los casos de este contrato es condición **necesaria pero no
suficiente**: la iteración se completa con el escenario de `banco.py` y la
revisión grupal.
