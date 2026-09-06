# Validaciones en Python: `re`, expresiones regulares, tipos y excepciones

## Objetivo

Este material trabaja una forma de organizar validaciones en Python separando:

- **la clase y su uso** en `principal_N.py`;
- **las funciones de validación** en `validaciones_N.py`.

La idea es que una clase no tenga que conocer todos los detalles de una expresión
regular o de una regla de validación. La clase pide que un dato sea validado y la
función correspondiente:

1. revisa el tipo;
2. normaliza el dato cuando corresponde;
3. revisa su contenido;
4. devuelve el valor válido;
5. o lanza una excepción si el dato no cumple el contrato.

---

# 1. ¿Qué es la librería `re`?

`re` es un módulo de la biblioteca estándar de Python para trabajar con
**expresiones regulares**.

Una expresión regular es un patrón que describe qué forma debe tener un texto.

Ejemplos:

```python
r"[0-9]{7,8}"
```

significa: entre 7 y 8 caracteres, y cada uno debe ser un dígito entre `0` y `9`.

```python
r"[A-Z]{3}[0-9]{3}"
```

significa: tres letras mayúsculas seguidas de tres dígitos.

Para usar el módulo:

```python
import re
```

No hay que instalarlo con `pip`, porque forma parte de Python.

## Comprobar un texto con `re.match()`

La forma más directa de comprobar si un texto cumple un patrón es `re.match()`:

```python
re.match(r"^[A-Z]{3}[0-9]{3}$", "ABC123")
```

`re.match()` intenta aplicar el patrón desde el comienzo del texto y devuelve un
objeto de coincidencia, o `None` si no coincide. Al encerrar el patrón entre `^`
y `$` exigimos que **todo** el texto cumpla la regla.

En el bloque 6 se explica en detalle cómo funciona `match()` y en el bloque 8 se
presenta `fullmatch()`, una variante más estricta.

## Nota sobre `{valor!r}` en los mensajes

En muchos mensajes de error vas a ver `f"...: {valor!r}"`. El sufijo `!r` muestra
el valor "tal cual" (con comillas y espacios visibles). Se explica en el
bloque 7; hasta entonces se puede leer como "mostrar el valor recibido".

---

# 2. `re.compile()` y el patrón de nombres

El patrón utilizado es:

```python
_PATRON_NOMBRE = re.compile(
    r"^[^\W\d_]+(?:[ '\-][^\W\d_]+)*$",
    re.UNICODE
)
```

`re.compile()` toma una expresión regular y crea un **objeto patrón reutilizable**.

En vez de escribir varias veces:

```python
re.match(r"...patron...", texto)
```

podemos preparar el patrón una vez:

```python
_PATRON_NOMBRE = re.compile(r"...patron...")
```

y luego usar:

```python
_PATRON_NOMBRE.match(texto)
```

Esto mejora la legibilidad cuando la misma regla se utiliza varias veces.

## Descomposición del patrón

```text
^
[^\W\d_]+
(?:[ '\-][^\W\d_]+)*
$
```

### `^`

Indica el **inicio del texto**.

### `[ ... ]`

Los corchetes definen una **clase de caracteres**.

### `^` dentro de `[ ... ]`

Dentro de los corchetes, `^` significa **negación**.

Por lo tanto:

```regex
[^\W\d_]
```

significa: aceptar un carácter que **no sea** ninguno de los indicados.

### `\W`

`\W` representa un carácter que no es considerado carácter de palabra.

Al negarlo mediante `[^...]`, aprovechamos el comportamiento Unicode de Python
para aceptar letras como:

```text
á é í ó ú ñ ü
Á É Í Ó Ú Ñ Ü
```

### `\d`

Representa un dígito.

Como aparece dentro de la negación:

```regex
[^\W\d_]
```

los dígitos quedan excluidos.

### `_`

También se excluye explícitamente el guion bajo.

### `+`

Significa **una o más repeticiones**.

Por eso:

```regex
[^\W\d_]+
```

representa una palabra formada por una o más letras.

### `(?: ... )`

Es un **grupo no capturante**.

Agrupa una parte del patrón, pero no necesitamos recuperar por separado el texto
que coincidió con ese grupo.

### `[ '\-]`

Acepta exactamente uno de estos separadores:

- espacio;
- apóstrofo;
- guion.

El guion se escribe como `\-` para dejar claro que se quiere representar el
carácter guion y no un rango.

### `*`

Significa **cero o más repeticiones**.

Entonces:

```regex
(?:[ '\-][^\W\d_]+)*
```

permite agregar cero o más palabras después de la primera.

Ejemplos válidos:

```text
Ana
María José
Juan Carlos
O'Connor
Ana-María
```

Ejemplos inválidos:

```text
Ana123
Juan_
María@
```

### `$`

Indica el **final del texto**.

La combinación:

```regex
^ ... $
```

exige que todo el texto cumpla el patrón.

### `re.UNICODE`

Indica que las categorías de caracteres se interpreten usando reglas Unicode.

En Python 3, el manejo Unicode ya es el comportamiento normal para cadenas
`str`, pero la marca hace explícita la intención del patrón.

## Los tres ejercicios de este bloque

El patrón final no aparece de golpe. Los tres ejercicios lo construyen por
partes:

1. `validaciones_1.py`: `^[^\W\d_]+$` — una sola palabra de letras.
2. `validaciones_2.py`: `^[^\W\d_]+(?: [^\W\d_]+)*$` — varias palabras separadas
   por un espacio.
3. `validaciones_3.py`: `^[^\W\d_]+(?:[ '\-][^\W\d_]+)*$` — además, apóstrofo y
   guion como separadores.

En este bloque la normalización se limita a `valor.strip()`. La sustitución de
espacios internos con `re.sub()` se agrega en el bloque 5.

---

# 3. `isinstance(valor, clase)`

`isinstance()` pregunta si un objeto pertenece a un determinado tipo.

Ejemplo:

```python
isinstance("Ana", str)
```

devuelve:

```python
True
```

En una validación:

```python
if not isinstance(valor, str):
    raise TypeError("El nombre debe ser str")
```

se está diciendo:

> Si `valor` no es un `str`, la función no puede continuar.

También puede comprobar varios tipos:

```python
isinstance(valor, (int, float))
```

Esto devuelve `True` si `valor` es un `int` **o** un `float`.

## `bool` es un caso especial

En Python, `bool` es una subclase de `int`. Por eso:

```python
isinstance(True, int)
```

devuelve `True`. Cuando una validación numérica no debe aceptar `True` ni
`False`, se agrega una comprobación explícita:

```python
if not isinstance(valor, int) or isinstance(valor, bool):
    raise TypeError("Se esperaba int")
```

Esto aparece en los ejercicios de este bloque y del bloque 4. El bloque 9 retoma
la idea con una función auxiliar `_es_numero()`.

---

# 4. `raise TypeError` y `raise ValueError`

`raise` significa **lanzar una excepción**.

## `TypeError`

Se usa cuando el problema es el **tipo del dato**.

```python
if not isinstance(valor, str):
    raise TypeError("El nombre debe ser str")
```

Ejemplo incorrecto:

```python
validar_nombre(123)
```

El problema no es que el nombre tenga caracteres inválidos: el problema es que
ni siquiera se recibió un texto.

## `ValueError`

Se usa cuando el tipo es correcto, pero el **contenido** no cumple la regla.

```python
raise ValueError("El nombre no puede quedar vacio")
```

El valor podría ser `str`, pero no es aceptable para el dominio.

Otros ejemplos:

```python
raise ValueError(
    f"Nombre con caracteres no permitidos: {valor!r}"
)
```

```python
raise ValueError(
    f"DNI invalido: {valor!r} (se esperan 7 u 8 digitos)"
)
```

## ¿Cómo se "captura" si no hay `except`?

Si no escribimos `try/except`, **no se captura**.

La excepción se propaga hacia la función que llamó a la validación.

Ejemplo:

```python
persona = Persona("Ana123", "Perez", "12345678")
```

Si el constructor llama a:

```python
validar_nombre("Ana123")
```

y esa función ejecuta:

```python
raise ValueError(...)
```

el `__init__` se interrumpe y la excepción continúa hacia el código que intentó
crear el objeto.

Si nadie la captura, Python:

1. detiene la ejecución;
2. muestra el tipo de excepción;
3. muestra el mensaje;
4. muestra el traceback.

Esto es útil durante el aprendizaje y durante las pruebas porque el error no
queda oculto.

---

# 5. `re.sub()` y la normalización de espacios

La línea:

```python
limpio = re.sub(r"\s+", " ", valor).strip()
```

hace dos operaciones.

## `re.sub(patron, reemplazo, texto)`

`sub` significa **substitute**, es decir, sustituir.

```python
re.sub(r"\s+", " ", valor)
```

busca uno o más caracteres de espacio en blanco y los reemplaza por un solo
espacio.

### `\s`

Representa caracteres de espacio en blanco, por ejemplo:

- espacio;
- tabulación;
- salto de línea.

### `+`

Significa uno o más.

Por lo tanto:

```regex
\s+
```

significa:

> uno o más caracteres de espacio en blanco consecutivos.

Ejemplo:

```python
valor = "  María    José  "
```

después de `re.sub(...)` queda aproximadamente:

```text
 María José 
```

Luego:

```python
.strip()
```

quita los espacios del principio y del final:

```text
María José
```

---

# 6. `.match()`

Ejemplo:

```python
if not _PATRON_NOMBRE.match(limpio):
    raise ValueError(...)
```

`match()` intenta comprobar el patrón comenzando desde el inicio del texto.

En este caso el patrón ya contiene:

```regex
^
```

al inicio y:

```regex
$
```

al final.

Por lo tanto, la expresión exige que el nombre completo cumpla la regla.

`match()` devuelve un objeto de coincidencia si el patrón se cumple y `None` si
no se cumple.

Por eso funciona:

```python
if not _PATRON_NOMBRE.match(limpio):
```

porque `None` se evalúa como falso.

## `match()` con `^ ... $` frente a `fullmatch()`

Anclar el patrón con `^` y `$` hace que `match()` exija prácticamente todo el
texto. Queda un único resquicio: `$` también coincide justo antes de un salto de
línea final, así que `"ABC123\n"` pasaría.

El bloque 8 presenta `re.fullmatch()`, que exige la coincidencia total sin
necesidad de escribir `^` ni `$` y sin esa excepción del salto de línea.

---

# 7. ¿Qué significa `{valor!r}`?

En una f-string:

```python
f"Valor invalido: {valor!r}"
```

`!r` indica que se utilice:

```python
repr(valor)
```

en lugar de la representación normal de `str(valor)`.

Ejemplo:

```python
valor = "  Ana  "
```

```python
print(f"{valor}")
```

muestra:

```text
  Ana
```

En cambio:

```python
print(f"{valor!r}")
```

muestra algo similar a:

```text
'  Ana  '
```

Esto es muy útil para mensajes de error porque permite ver:

- comillas;
- espacios iniciales;
- espacios finales;
- caracteres especiales.

---

# 8. `re.fullmatch()` y las cadenas crudas `r"..."`

Ejemplo:

```python
re.fullmatch(r"[0-9]{7,8}", valor)
```

`fullmatch()` exige que **todo el texto** coincida con el patrón.

No alcanza con que exista una parte válida.

A diferencia de `match()` con `^ ... $` (bloque 6), con `fullmatch()` no hace
falta escribir los anclajes y tampoco se cuela un salto de línea final. Por eso,
para validar un valor completo, suele ser la opción más clara.

Ejemplos:

```python
re.fullmatch(r"[0-9]{7,8}", "12345678")
```

coincide.

```python
re.fullmatch(r"[0-9]{7,8}", "DNI12345678")
```

no coincide.

## `[0-9]`

Acepta un dígito entre `0` y `9`.

## `{7,8}`

Indica una cantidad mínima y máxima:

```text
7 u 8 repeticiones
```

## ¿Por qué se usa `r`?

La letra `r` delante del string crea una **raw string** o cadena cruda:

```python
r"[0-9]{7,8}"
```

En una cadena normal, la barra invertida `\` también tiene significado para
Python.

Las expresiones regulares usan muchas barras invertidas:

```regex
\d
\s
\w
```

La cadena cruda evita que tengamos que escapar continuamente esas barras.

Por eso suele escribirse:

```python
r"\s+"
r"\d{8}"
r"[A-Z]\d+"
```

Es una buena práctica para escribir expresiones regulares legibles.

---

# 9. Función `_es_numero()`

```python
def _es_numero(valor):
    # bool es subclase de int: lo excluimos explicitamente.
    return isinstance(valor, (int, float)) and not isinstance(valor, bool)
```

La función devuelve una expresión booleana.

Primero pregunta:

```python
isinstance(valor, (int, float))
```

Es decir:

> ¿el valor es entero o flotante?

Pero existe un detalle importante de Python:

```python
isinstance(True, int)
```

devuelve `True`.

Esto ocurre porque `bool` es una subclase de `int`.

Para una validación de dinero normalmente no queremos aceptar:

```python
True
False
```

como si fueran números.

Por eso agregamos:

```python
and not isinstance(valor, bool)
```

El resultado final es:

```text
10       -> True
10.5     -> True
True     -> False
False    -> False
"10"     -> False
```

El guion bajo inicial:

```python
_es_numero
```

es una convención que indica:

> esta función es auxiliar o de uso interno del módulo.

No la vuelve privada de forma estricta.

---

# 10. Una función que usa otra función

Ejemplo:

```python
def validar_saldo_inicial(valor):
    if not _es_numero(valor):
        raise TypeError("El saldo inicial debe ser int o float")

    if valor < 0:
        raise ValueError("El saldo inicial no puede ser negativo")

    return valor
```

La función `validar_saldo_inicial()` delega una parte de su trabajo a:

```python
_es_numero(valor)
```

Esto evita repetir:

```python
isinstance(valor, (int, float)) and not isinstance(valor, bool)
```

en muchas funciones.

Podríamos reutilizarla en:

```python
validar_saldo_inicial()
validar_monto()
validar_precio()
validar_limite()
```

Esto mejora:

- reutilización;
- legibilidad;
- mantenimiento;
- consistencia.

Si después cambiara la definición de "número válido", habría que modificar una
sola función.

---

# 11. Flujo completo de una validación

Ejemplo:

```python
def validar_nombre(valor):
    if not isinstance(valor, str):
        raise TypeError("El nombre debe ser str")

    limpio = re.sub(r"\s+", " ", valor).strip()

    if not limpio:
        raise ValueError("El nombre no puede quedar vacio")

    if not _PATRON_NOMBRE.match(limpio):
        raise ValueError(
            f"Nombre con caracteres no permitidos: {valor!r}"
        )

    return limpio.title()
```

El flujo es:

```text
dato recibido
    |
    v
¿tipo correcto?
    |
    +-- no --> TypeError
    |
    v
normalizar
    |
    v
¿quedó vacío?
    |
    +-- sí --> ValueError
    |
    v
¿cumple el patrón?
    |
    +-- no --> ValueError
    |
    v
devolver valor normalizado
```

## Sobre normalizar o no

No todos los validadores normalizan. Algunos devuelven el valor tal cual
(`return valor`); otros lo transforman antes de devolverlo (`.strip()`,
`.title()`, `float(valor)`). Es una decisión de diseño de cada regla, no una
obligación: conviene ser coherente dentro de un mismo proyecto.

## Sobre `.title()`

`.title()` pone en mayúscula la primera letra de cada palabra. Funciona bien
para nombres simples (`"maría josé"` -> `"María José"`), pero no para casos como
`"McLeod"` (quedaría `"Mcleod"`). Para este material alcanza; un sistema real
usaría una normalización más cuidadosa.

---

# 12. Organización recomendada

Ejemplo:

```text
principal_1.py
validaciones_1.py
```

En `validaciones_1.py`:

```python
def validar_nombre(...):
    ...
```

En `principal_1.py`:

```python
from validaciones_1 import validar_nombre
```

La clase utiliza la función:

```python
class Persona:
    def __init__(self, nombre):
        self.__nombre = validar_nombre(nombre)
```

Así se separan responsabilidades:

```text
Persona
    -> representa una entidad

validar_nombre()
    -> representa una regla de validación
```

---

# 13. Secuencia de ejercicios

Este paquete contiene 10 bloques conceptuales.

Cada bloque tiene tres ejercicios:

```text
principal_1.py + validaciones_1.py
principal_2.py + validaciones_2.py
principal_3.py + validaciones_3.py
```

Los ejercicios son intencionalmente breves. Cada uno define una clase cuyos
atributos deben pasar por funciones de validación.

Los bloques están pensados para leerse en orden: cada uno usa solo lo visto en
los bloques anteriores. Cuando un ejercicio anticipa una construcción, la guía
lo señala.

## Bloques

1. `re` y patrones básicos (`re.match()` con `^ ... $`).
2. `re.compile()` y construcción del patrón de nombres en tres pasos.
3. `isinstance()` y `bool` como subclase de `int`.
4. `raise TypeError` y `raise ValueError` sin `except`.
5. `re.sub()` y normalización de espacios internos.
6. `match()` y su relación con `fullmatch()`.
7. `!r` en mensajes de error.
8. `fullmatch()` y raw strings.
9. `_es_numero()` y exclusión de `bool`.
10. Una función de validación que reutiliza otra función.

---

# 14. Recomendación didáctica

Para cada ejercicio conviene pedir al estudiante que:

1. lea primero `principal_N.py`;
2. identifique qué atributos necesitan validación;
3. escriba o complete `validaciones_N.py`;
4. ejecute con valores válidos;
5. descomente un caso inválido;
6. observe qué excepción se genera;
7. explique por qué corresponde `TypeError` o `ValueError`;
8. modifique un patrón y prediga qué entradas comenzarán a aceptarse o rechazarse.

No es necesario usar `try/except` para aprender estas validaciones. Al principio
es incluso útil permitir que la excepción llegue a consola para observar el
traceback y entender en qué punto se interrumpió el programa.
