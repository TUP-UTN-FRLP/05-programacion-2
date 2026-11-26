# Funciones Utilizadas en capitulo_03_Condicional

Documento que agrupa las funciones built-in y los métodos utilizados en los
ejercicios y enunciados, organizados por tipo de dato y en orden alfabético.

---

## Funciones Generales

### `float(valor)`

**¿Qué realiza?**

Convierte un valor compatible en un número de punto flotante (`float`).
Por ejemplo, puede convertir un string que representa un número o un
número entero.

El string debe utilizar un formato numérico válido para Python. Por ejemplo,
`"3.14"` es válido, pero `"3,14"` no lo es.

**¿Qué retorna?**

Un valor de tipo `float`.

**Ejemplos típicos:**

```python
float("3.14")                       # Retorna 3.14
float(5)                            # Retorna 5.0
precio = float(input("Precio: "))   # Convierte la entrada a float
float("-2.5")                       # Retorna -2.5
```

### `input(mensaje)`

**¿Qué realiza?**

Solicita una entrada al usuario desde la entrada estándar. Muestra un
mensaje y espera que el usuario escriba un valor.

**¿Qué retorna?**

Un valor de tipo `str` con los caracteres ingresados por el usuario.

`input()` siempre retorna un string, aunque el usuario ingrese un número.

**Ejemplos típicos:**

```python
nombre = input("¿Cuál es tu nombre? ")    # Retorna un str
numero = input("Ingresa un número: ")      # Retorna un str
respuesta = input("¿Continuar? (s/n): ")  # Retorna un str
```

### `int(valor)`

**¿Qué realiza?**

Convierte un valor compatible en un número entero (`int`).

Cuando recibe un número de punto flotante, elimina la parte decimal
truncando hacia cero. No realiza un redondeo.

**¿Qué retorna?**

Un valor de tipo `int`.

**Ejemplos típicos:**

```python
int("42")                         # Retorna 42
int(3.14)                         # Retorna 3
int(-3.14)                        # Retorna -3
edad = int(input("Tu edad: "))    # Convierte la entrada a int
```

### `max(colección)` o `max(a, b, c, ...)`

**¿Qué realiza?**

Retorna el elemento de mayor valor de una colección o el mayor entre
varios argumentos.

Los elementos comparados deben ser compatibles entre sí.

**¿Qué retorna?**

El elemento de mayor valor.

**Ejemplos típicos:**

```python
max([3, 1, 4, 1, 5])          # Retorna 5
max("abc")                    # Retorna "c"
max(10, 20, 5)                # Retorna 20
max(["Ana", "Juan", "Zoe"])   # Retorna "Zoe"
```

Cuando se comparan strings, Python utiliza el orden de los valores Unicode.
Por lo tanto, no debe interpretarse necesariamente como un orden alfabético
según las reglas de un idioma.

### `print(*objetos, sep=' ', end='\n')`

**¿Qué realiza?**

Escribe uno o varios valores en la salida estándar. Por defecto, la salida
se dirige a la consola.

El parámetro `sep` permite definir el separador entre los valores y `end`
permite definir qué se escribe al finalizar.

**¿Qué retorna?**

`None`.

**Ejemplos típicos:**

```python
print("Hola")                 # Imprime: Hola
print(42)                     # Imprime: 42
print("Nombre:", "Juan")      # Imprime: Nombre: Juan
print(1, 2, 3, sep="-")       # Imprime: 1-2-3
print("Sin salto", end="")    # No agrega salto de línea
```

---

## Métodos de Strings (Cadenas de Texto)

Los siguientes elementos son métodos de la clase `str`. Se invocan sobre
un objeto de tipo string, por ejemplo, `texto.lower()`.

### Una idea fundamental: un string está formado por caracteres

Un string no debe confundirse con un número.

Por ejemplo:

```python
"99"
```

es un string formado por **dos caracteres**:

```text
┌───┬───┐
│ 9 │ 9 │
└───┴───┘
  0   1
```

Podemos acceder individualmente a esos caracteres:

```python
texto = "99"

print(texto[0])    # 9
print(texto[1])    # 9
```

Por lo tanto, cuando utilizamos métodos como `isdecimal()`, `isdigit()` o
`isnumeric()`, no estamos preguntando si el string completo representa un
número dentro de un determinado rango.

Estamos preguntando si **cada uno de sus caracteres** cumple una determinada
propiedad.

Por ejemplo:

```python
"99".isdecimal()       # True
```

No significa:

> "99 está entre 0 y 9".

Significa:

> "El primer carácter es decimal y el segundo carácter también es decimal".

Por eso:

```python
"9".isdecimal()        # True
"99".isdecimal()       # True
"123456".isdecimal()   # True
"123a".isdecimal()     # False
```

Esta diferencia es fundamental para comprender los métodos `is...()` de
strings.

---

### `string.isalpha()`

**¿Qué realiza?**

Verifica si todos los caracteres del string son caracteres alfabéticos.

No se limita a las letras `A-Z` y `a-z`; también reconoce letras de otros
alfabetos y determinados caracteres Unicode.

**¿Qué retorna?**

`True` si el string no está vacío y todos sus caracteres son alfabéticos.
`False` en caso contrario.

**Ejemplos típicos:**

```python
"abc".isalpha()       # Retorna True
"Árbol".isalpha()     # Retorna True
"123".isalpha()       # Retorna False
"abc123".isalpha()    # Retorna False
"".isalpha()          # Retorna False
```

### `string.isalnum()`

**¿Qué realiza?**

Verifica si todos los caracteres del string son alfabéticos o numéricos.

Un carácter se considera numérico cuando pertenece a alguna de las
categorías reconocidas por los métodos numéricos de strings.

Los espacios, signos de puntuación y otros caracteres que no sean
alfabéticos o numéricos hacen que el resultado sea `False`.

**¿Qué retorna?**

`True` si el string no está vacío y todos sus caracteres son alfanuméricos.
`False` en caso contrario.

**Ejemplos típicos:**

```python
"ABC".isalnum()        # Retorna True
"123".isalnum()        # Retorna True
"ABC123".isalnum()     # Retorna True
"ABC 123".isalnum()    # Retorna False
"ABC-123".isalnum()    # Retorna False
"".isalnum()           # Retorna False
```

### `string.isdecimal()`

**¿Qué realiza?**

Verifica si todos los caracteres del string son caracteres decimales
Unicode.

Los caracteres decimales son los que pertenecen a la categoría Unicode
`Numeric_Type=Decimal`.

Los caracteres `0` a `9` son ejemplos de caracteres decimales, pero no son
los únicos caracteres decimales existentes.

**¿Qué retorna?**

`True` si el string no está vacío y todos sus caracteres son decimales.
`False` en caso contrario.

**Ejemplos típicos:**

```python
"123".isdecimal()       # Retorna True
"99".isdecimal()        # Retorna True
"٠١٢".isdecimal()      # Retorna True
"²".isdecimal()         # Retorna False
"⅕".isdecimal()         # Retorna False
"12.3".isdecimal()      # Retorna False
"".isdecimal()          # Retorna False
```

Es importante observar que:

```python
"99".isdecimal()
```

da `True` porque **cada uno de los dos caracteres**, `"9"` y `"9"`, es
decimal.

No se está comparando el valor `99` con el intervalo `0..9`.

### `string.isdigit()`

**¿Qué realiza?**

Verifica si todos los caracteres del string son caracteres que Unicode
considera dígitos.

Incluye los caracteres reconocidos por `isdecimal()` y también algunos
caracteres Unicode clasificados específicamente como dígitos.

Por eso, `isdigit()` reconoce un conjunto más amplio de caracteres que
`isdecimal()`.

**¿Qué retorna?**

`True` si el string no está vacío y todos sus caracteres son dígitos.
`False` en caso contrario.

**Ejemplos típicos:**

```python
"123".isdigit()       # Retorna True
"99".isdigit()        # Retorna True
"٠١٢".isdigit()       # Retorna True
"²".isdigit()         # Retorna True
"⅕".isdigit()         # Retorna False
"12.3".isdigit()      # Retorna False
"".isdigit()          # Retorna False
```

### `string.isnumeric()`

**¿Qué realiza?**

Verifica si todos los caracteres del string son caracteres numéricos según
Unicode.

Es el método más amplio de los tres métodos relacionados con caracteres
decimales, dígitos y caracteres numéricos.

Incluye caracteres decimales, otros dígitos y caracteres que representan
valores numéricos, como determinadas fracciones y números romanos.

**¿Qué retorna?**

`True` si el string no está vacío y todos sus caracteres son numéricos.
`False` en caso contrario.

**Ejemplos típicos:**

```python
"123".isnumeric()       # Retorna True
"99".isnumeric()        # Retorna True
"²".isnumeric()         # Retorna True
"⅕".isnumeric()         # Retorna True
"Ⅻ".isnumeric()         # Retorna True
"12.3".isnumeric()      # Retorna False
"".isnumeric()          # Retorna False
```

### Relación entre `isdecimal()`, `isdigit()` e `isnumeric()`

Los tres métodos están relacionados, pero no reconocen exactamente los
mismos caracteres.

La relación de inclusión entre los conjuntos de caracteres que reconoce
cada método es:

```text
isdecimal() ⊂ isdigit() ⊂ isnumeric()
```

Puede representarse conceptualmente así:

```text
                    isnumeric()
        ┌─────────────────────────────┐
        │                             │
        │          isdigit()          │
        │      ┌───────────────┐      │
        │      │               │      │
        │      │ isdecimal()   │      │
        │      │               │      │
        │      └───────────────┘      │
        │                             │
        │  Otros caracteres          │
        │  numéricos                  │
        │                             │
        └─────────────────────────────┘
```

Esto significa:

* Todo carácter decimal también es considerado un dígito.
* Todo carácter considerado dígito también es considerado numérico.
* No todo carácter numérico es un dígito.
* No todo dígito es un carácter decimal.

Una comparación:

| Carácter | `isdecimal()` | `isdigit()` | `isnumeric()` |
| -------- | ------------: | ----------: | ------------: |
| `"5"`    |        `True` |      `True` |        `True` |
| `"99"`   |        `True` |      `True` |        `True` |
| `"٥"`    |        `True` |      `True` |        `True` |
| `"²"`    |       `False` |      `True` |        `True` |
| `"⅕"`    |       `False` |     `False` |        `True` |
| `"Ⅻ"`    |       `False` |     `False` |        `True` |
| `"A"`    |       `False` |     `False` |       `False` |

**Importante:** la relación de inclusión se refiere a los **conjuntos de
caracteres reconocidos** por cada método.

Cuando el método se aplica a un string, el resultado es `True` solamente
si **todos los caracteres del string** pertenecen al conjunto correspondiente
y el string no está vacío.

Por ejemplo:

```python
"123".isdecimal()     # True
"123a".isdecimal()    # False
```

En el segundo caso, `"1"`, `"2"` y `"3"` son caracteres decimales, pero
`"a"` no lo es. Como no todos los caracteres cumplen la condición, el
resultado es `False`.

---

### Los métodos `is...()` no validan números

Es importante no interpretar:

```python
"123".isdigit()
```

como:

> "123 es un número".

El método está analizando los **caracteres del string**.

Por ejemplo:

```python
"123".isdigit()       # True
"-123".isdigit()      # False
"+123".isdigit()      # False
"12.5".isdigit()      # False
```

`123`, `-123`, `+123` y `12.5` pueden representar números, pero contienen
caracteres diferentes.

El signo `-` no es un dígito, el signo `+` tampoco y el punto `.` tampoco.

Por eso estos métodos no son, por sí solos, una forma general de validar
si una entrada representa un número válido para `int()` o `float()`.

---

### `string.lower()`

**¿Qué realiza?**

Devuelve una versión del string en la que los caracteres que tienen una
correspondencia en minúscula se convierten a minúsculas.

**¿Qué retorna?**

Un nuevo string.

El string original no se modifica porque los strings de Python son
inmutables.

**Ejemplos típicos:**

```python
"PYTHON".lower()                   # Retorna "python"
"HeLLo WoRLd".lower()              # Retorna "hello world"

entrada = input("¿Continuar? ").lower()

if entrada == "s":
    # Continuar
```

### `string.replace(viejo, nuevo)`

**¿Qué realiza?**

Devuelve un nuevo string en el que las ocurrencias de una subcadena se
reemplazan por otra.

Por defecto, reemplaza todas las ocurrencias. Se puede indicar un tercer
argumento para establecer la cantidad máxima de reemplazos.

**¿Qué retorna?**

Un nuevo string con los reemplazos realizados.

El string original no se modifica.

**Ejemplos típicos:**

```python
"Python es genial".replace("genial", "excelente")
# Retorna "Python es excelente"

"aaa".replace("a", "b")    # Retorna "bbb"

texto = "hola hola".replace("hola", "adiós")
# Retorna "adiós adiós"

"aaa".replace("a", "b", 2)
# Retorna "bba"
```

### `string.strip()`

**¿Qué realiza?**

Devuelve un nuevo string eliminando los caracteres de espacio en blanco
que se encuentran al principio y al final.

Por defecto, elimina caracteres como espacios, tabulaciones y saltos de
línea.

Si se proporciona un argumento, este se interpreta como un conjunto de
caracteres que pueden eliminarse de los extremos. No se interpreta como
una subcadena completa.

**¿Qué retorna?**

Un nuevo string sin los caracteres indicados en sus extremos.

El string original no se modifica.

**Ejemplos típicos:**

```python
"  Python  ".strip()     # Retorna "Python"
"\thello\n".strip()      # Retorna "hello"

entrada = input("Nombre: ").strip()

"  123  ".strip()        # Retorna "123"
```

### `string.upper()`

**¿Qué realiza?**

Devuelve una versión del string en la que los caracteres que tienen una
correspondencia en mayúscula se convierten a mayúsculas.

**¿Qué retorna?**

Un nuevo string.

El string original no se modifica porque los strings de Python son
inmutables.

**Ejemplos típicos:**

```python
"python".upper()                  # Retorna "PYTHON"
"HeLLo WoRLd".upper()             # Retorna "HELLO WORLD"
mensaje = "Atención".upper()      # Retorna "ATENCIÓN"
```

---

## Resumen por Categoría

| Categoría              | Elementos                                                                     |
| ---------------------- | ----------------------------------------------------------------------------- |
| **Funciones built-in** | float, input, int, max, print                                                 |
| **Métodos de `str`**   | isalpha, isalnum, isdecimal, isdigit, isnumeric, lower, replace, strip, upper |

---

## Notas Importantes

* **Funciones vs. métodos:** Las funciones built-in se invocan directamente,
  por ejemplo, `float(valor)` o `print(valor)`. Los métodos se invocan sobre
  un objeto, por ejemplo, `texto.lower()`.

* **Strings como secuencias:** Un string es una secuencia de caracteres.
  Puede recorrerse, indexarse y consultarse carácter por carácter.

```python
texto = "Hola"

print(texto[0])    # H
print(texto[1])    # o
print(texto[2])    # l
print(texto[3])    # a
```

* **Strings inmutables:** Los strings de Python son inmutables. Métodos como
  `lower()`, `upper()`, `replace()` y `strip()` no modifican el string
  original; devuelven un nuevo string.

* **Asignación del resultado:** Si se desea conservar el resultado de un
  método de string, se debe asignar a una variable.

```python
texto = "HOLA"

texto.lower()

print(texto)       # HOLA

texto = texto.lower()

print(texto)       # hola
```

* **Métodos `is...()`:** Los métodos como `isalpha()`, `isalnum()`,
  `isdecimal()`, `isdigit()` e `isnumeric()` realizan una clasificación de
  los caracteres de un string. No convierten el string a otro tipo de dato.

* **Strings vacíos:** Los métodos de este grupo retornan `False` cuando se
  aplican a un string vacío. Por ejemplo:

```python
"".isalpha()       # False
"".isalnum()       # False
"".isdecimal()     # False
"".isdigit()       # False
"".isnumeric()     # False
```

* **PEP 8:** PEP 8 es la guía de estilo para código Python. Entre sus
  recomendaciones se encuentra limitar a 79 caracteres las líneas de
  código y a 72 caracteres las líneas de comentarios y docstrings. Estas
  recomendaciones corresponden al código Python y no constituyen una regla
  obligatoria para los archivos Markdown.

* **Importancia de estas funciones y métodos:** Son herramientas
  fundamentales para trabajar con conversiones de datos, entrada y salida,
  validaciones y manipulación de strings en Python.
