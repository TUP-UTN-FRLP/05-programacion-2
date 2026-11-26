# Funciones Utilizadas en capitulo_06_Funciones

Documento que agrupa las funciones built-in, los métodos y las
construcciones del lenguaje utilizados en los ejercicios y enunciados,
organizados por tipo y en orden alfabético.

---

## Funciones Generales

### `help(objeto)`

**¿Qué realiza?**

Muestra la documentación de ayuda de un objeto, función, módulo o
clase. Cuando se aplica a una función definida con un docstring,
muestra ese docstring junto con la firma de la función.

**¿Qué retorna?**

`None`. La información se imprime en la salida estándar.

**Ejemplos típicos:**

```python
help(print)             # Muestra la ayuda de la función print
help(calcular_precio)   # Muestra el docstring de la función
help(str)               # Muestra la ayuda de la clase str
```

### `input(mensaje)`

**¿Qué realiza?**

Solicita una entrada al usuario desde la entrada estándar. Muestra un
mensaje y espera que el usuario escriba un valor.

**¿Qué retorna?**

Un valor de tipo `str` con los caracteres ingresados por el usuario.

`input()` siempre retorna un string, aunque el usuario ingrese un
número.

**Ejemplos típicos:**

```python
nombre = input("¿Cuál es tu nombre? ")   # Retorna un str
numero = input("Ingresa un número: ")     # Retorna un str
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
int("42")                        # Retorna 42
int(3.14)                        # Retorna 3
int(-3.14)                       # Retorna -3
edad = int(input("Tu edad: "))   # Convierte la entrada a int
```

### `len(colección)`

**¿Qué realiza?**

Retorna la cantidad de elementos de una colección o la longitud de un
string.

Funciona con listas, tuplas, diccionarios, strings y cualquier objeto
que implemente la interfaz de secuencia o colección.

**¿Qué retorna?**

Un valor de tipo `int`.

**Ejemplos típicos:**

```python
len([1, 2, 3])       # Retorna 3
len("Hola")          # Retorna 4
len({})              # Retorna 0
len((1, 2, 3, 4))    # Retorna 4
```

### `max(colección)` o `max(a, b, c, ...)`

**¿Qué realiza?**

Retorna el elemento de mayor valor de una colección o el mayor entre
varios argumentos.

Acepta un argumento `key` para especificar una función que se aplica
a cada elemento antes de la comparación.

**¿Qué retorna?**

El elemento de mayor valor. Cuando se usa `key=`, retorna el elemento
original, no el resultado de aplicar la función `key`.

**Ejemplos típicos:**

```python
max([3, 1, 4, 1, 5])                     # Retorna 5
max(10, 20, 5)                            # Retorna 20
max(["Ana", "Juan", "Zoe"])               # Retorna "Zoe"

productos = [("pan", 500), ("leche", 800)]
max(productos, key=lambda p: p[1])        # Retorna ("leche", 800)
```

Cuando se comparan strings, Python utiliza el orden de los valores
Unicode. Por lo tanto, no debe interpretarse necesariamente como un
orden alfabético según las reglas de un idioma.

### `min(colección)` o `min(a, b, c, ...)`

**¿Qué realiza?**

Retorna el elemento de menor valor de una colección o el menor entre
varios argumentos.

Al igual que `max()`, acepta un argumento `key` para personalizar el
criterio de comparación.

**¿Qué retorna?**

El elemento de menor valor. Cuando se usa `key=`, retorna el elemento
original, no el resultado de aplicar la función `key`.

**Ejemplos típicos:**

```python
min([3, 1, 4, 1, 5])          # Retorna 1
min(10, 20, 5)                 # Retorna 5
mi, ma = min(nums), max(nums)  # Mínimo y máximo en una línea
```

### `print(*objetos, sep=' ', end='\n')`

**¿Qué realiza?**

Escribe uno o varios valores en la salida estándar. Por defecto, la
salida se dirige a la consola.

El parámetro `sep` permite definir el separador entre los valores y
`end` permite definir qué se escribe al finalizar.

**¿Qué retorna?**

`None`.

**Ejemplos típicos:**

```python
print("Hola")                 # Imprime: Hola
print(42)                     # Imprime: 42
print(1, 2, 3, sep="-")       # Imprime: 1-2-3
print("Sin salto", end="")    # No agrega salto de línea
print(numero, end=" ")        # Imprime el número seguido de un espacio
```

### `range(inicio, fin, paso)`

**¿Qué realiza?**

Genera una secuencia de enteros. Permite uno, dos o tres argumentos:

- `range(fin)`: desde `0` hasta `fin - 1`.
- `range(inicio, fin)`: desde `inicio` hasta `fin - 1`.
- `range(inicio, fin, paso)`: desde `inicio` hasta `fin - 1`, de
  `paso` en `paso`.

**¿Qué retorna?**

Un objeto `range`, que es iterable pero no una lista. Se puede
convertir con `list(range(...))`.

**Ejemplos típicos:**

```python
range(1, 11)              # 1, 2, 3, ..., 10
range(1, n + 1)           # 1 hasta n inclusive
range(2, n)               # 2 hasta n - 1
range(3, limite + 1, 2)   # 3, 5, 7, ... hasta limite
```

### `sorted(iterable, key=None, reverse=False)`

**¿Qué realiza?**

Retorna una nueva lista con los elementos del iterable ordenados.

El argumento `key` acepta una función que se aplica a cada elemento
antes de comparar. El argumento `reverse=True` invierte el orden
(descendente).

**¿Qué retorna?**

Una nueva lista ordenada. El iterable original no se modifica.

**Ejemplos típicos:**

```python
sorted([3, 1, 4, 1, 5])                    # Retorna [1, 1, 3, 4, 5]
sorted([3, 1, 4], reverse=True)             # Retorna [4, 3, 1]

productos = [("pan", 500), ("leche", 800)]
sorted(productos, key=lambda p: p[1])
# Retorna [("pan", 500), ("leche", 800)]

notas = {"Ana": 8, "Juan": 6}
sorted(notas.items(), key=lambda par: par[1], reverse=True)
# Retorna [("Ana", 8), ("Juan", 6)]
```

### `sum(iterable)`

**¿Qué realiza?**

Retorna la suma de los elementos de un iterable numérico.

**¿Qué retorna?**

La suma total. El tipo del resultado depende de los elementos del
iterable.

**Ejemplos típicos:**

```python
sum([1, 2, 3, 4])             # Retorna 10
sum([7, 3, 9, 5, 8])          # Retorna 32
promedio = sum(nums) / len(nums)
```

---

## Métodos de Strings (Cadenas de Texto)

Los siguientes elementos son métodos de la clase `str`. Se invocan
sobre un objeto de tipo string, por ejemplo, `texto.lower()`.

### `string.center(ancho)`

**¿Qué realiza?**

Devuelve un nuevo string centrado dentro de un campo de `ancho`
caracteres. Los espacios sobrantes se distribuyen a ambos lados. Por
defecto, el relleno se realiza con espacios.

**¿Qué retorna?**

Un nuevo string de longitud `ancho`. Si el string original es más largo
que `ancho`, se retorna sin modificar.

**Ejemplos típicos:**

```python
"Hola".center(10)           # Retorna "   Hola   "
"Python".center(10)         # Retorna "  Python  "
texto.upper().center(30)    # Centra el texto en mayúsculas
```

### `string.isdigit()`

**¿Qué realiza?**

Verifica si todos los caracteres del string son caracteres que Unicode
considera dígitos.

Incluye los dígitos decimales del `0` al `9` y también algunos
caracteres Unicode clasificados específicamente como dígitos, como
los superíndices `²`, `³`.

**¿Qué retorna?**

`True` si el string no está vacío y todos sus caracteres son dígitos.
`False` en caso contrario.

**Ejemplos típicos:**

```python
"123".isdigit()      # Retorna True
"99".isdigit()       # Retorna True
"²".isdigit()        # Retorna True
"12.3".isdigit()     # Retorna False
"-123".isdigit()     # Retorna False
"".isdigit()         # Retorna False
```

Es importante recordar que `isdigit()` no valida si el string
representa un número con signo o decimal. El signo `-` y el punto `.`
no son dígitos.

### `string.lower()`

**¿Qué realiza?**

Devuelve una versión del string en la que los caracteres que tienen una
correspondencia en minúscula se convierten a minúsculas.

**¿Qué retorna?**

Un nuevo string. El string original no se modifica porque los strings
de Python son inmutables.

**Ejemplos típicos:**

```python
"PYTHON".lower()                     # Retorna "python"
"HeLLo WoRLd".lower()                # Retorna "hello world"
texto.lower().split()                # Normaliza antes de separar
n.lower().startswith(letra.lower())  # Compara sin importar mayúsculas
```

### `string.replace(viejo, nuevo)`

**¿Qué realiza?**

Devuelve un nuevo string en el que las ocurrencias de `viejo` se
reemplazan por `nuevo`.

Por defecto, reemplaza todas las ocurrencias. Se puede indicar un
tercer argumento para establecer la cantidad máxima de reemplazos.

**¿Qué retorna?**

Un nuevo string con los reemplazos realizados. El string original no
se modifica.

**Ejemplos típicos:**

```python
"hola hola".replace("hola", "adiós")   # Retorna "adiós adiós"
texto.lower().replace(" ", "")          # Elimina todos los espacios
"aaa".replace("a", "b", 2)             # Retorna "bba"
```

### `string.split(sep=None)`

**¿Qué realiza?**

Divide el string en una lista de subcadenas utilizando `sep` como
separador. Si `sep` es `None` (o se omite), divide por espacios en
blanco y descarta los fragmentos vacíos resultantes.

**¿Qué retorna?**

Una lista de strings.

**Ejemplos típicos:**

```python
"el gato y el perro".split()
# Retorna ["el", "gato", "y", "el", "perro"]

"a,b,c".split(",")             # Retorna ["a", "b", "c"]
texto.lower().split()          # Divide en palabras normalizadas
```

### `string.startswith(prefijo)`

**¿Qué realiza?**

Verifica si el string comienza con el prefijo indicado.

**¿Qué retorna?**

`True` si el string comienza con `prefijo`. `False` en caso contrario.

**Ejemplos típicos:**

```python
"Ana".startswith("A")                   # Retorna True
"Python".startswith("py")               # Retorna False
n.lower().startswith(letra.lower())     # Comparación normalizada
```

### `string.upper()`

**¿Qué realiza?**

Devuelve una versión del string en la que los caracteres que tienen una
correspondencia en mayúscula se convierten a mayúsculas.

**¿Qué retorna?**

Un nuevo string. El string original no se modifica porque los strings
de Python son inmutables.

**Ejemplos típicos:**

```python
"python".upper()                 # Retorna "PYTHON"
"HeLLo WoRLd".upper()            # Retorna "HELLO WORLD"
texto.upper().center(30)         # Convierte a mayúsculas y centra
```

---

## Métodos de Listas

Los siguientes elementos son métodos de la clase `list`. Se invocan
sobre un objeto de tipo lista, por ejemplo, `mi_lista.append(x)`.

### `list.append(elemento)`

**¿Qué realiza?**

Agrega `elemento` al final de la lista, modificando la lista en el
lugar.

**¿Qué retorna?**

`None`. La lista se modifica directamente.

**Ejemplos típicos:**

```python
resultado = []
resultado.append(x * 2)   # Agrega el doble de x al final

nombres = []
nombres.append("Ana")     # Agrega "Ana" al final de la lista
```

---

## Métodos de Diccionarios

Los siguientes elementos son métodos de la clase `dict`. Se invocan
sobre un objeto de tipo diccionario.

### `dict.get(clave, default=None)`

**¿Qué realiza?**

Retorna el valor asociado a `clave` si esta existe en el diccionario.
Si `clave` no existe, retorna `default` en lugar de lanzar un error
`KeyError`.

**¿Qué retorna?**

El valor asociado a `clave`, o `default` si la clave no existe.
Por defecto, `default` es `None`.

**Ejemplos típicos:**

```python
saludos = {"es": "Hola", "en": "Hello"}
saludos.get("es", "Hola")   # Retorna "Hola"
saludos.get("fr", "Hola")   # Retorna "Hola" (clave no existe)

contador.get(palabra, 0)    # Retorna 0 si la palabra no está
```

### `dict.items()`

**¿Qué realiza?**

Retorna una vista de los pares clave-valor del diccionario, como una
secuencia de tuplas `(clave, valor)`.

**¿Qué retorna?**

Un objeto `dict_items`. Es iterable y refleja el estado actual del
diccionario.

**Ejemplos típicos:**

```python
notas = {"Ana": 8, "Juan": 6}

for nombre, nota in notas.items():
    print(nombre, nota)

sorted(notas.items(), key=lambda par: par[1], reverse=True)
# Ordena por el valor (nota) de mayor a menor
```

### `dict.update(otro_dict)`

**¿Qué realiza?**

Incorpora los pares clave-valor de `otro_dict` al diccionario. Si una
clave ya existe, su valor se sobreescribe.

**¿Qué retorna?**

`None`. El diccionario se modifica directamente.

**Ejemplos típicos:**

```python
ficha = {"nombre": "Ana", "edad": 25}
ficha.update({"carrera": "Ingeniería", "ciudad": "La Plata"})
# ficha ahora tiene cuatro claves

ficha.update(datos_extra)   # datos_extra puede venir de **kwargs
```

---

## Módulo `math`

### `math.isqrt(n)`

**¿Qué realiza?**

Retorna la raíz cuadrada entera de `n`, es decir, el mayor entero `k`
tal que `k² ≤ n`.

Es la forma recomendada cuando se necesita la raíz entera exacta,
porque evita los errores de redondeo que pueden producirse al usar
`int(math.sqrt(n))` con números de punto flotante.

Requiere `import math`.

**¿Qué retorna?**

Un valor de tipo `int`.

**Ejemplos típicos:**

```python
import math

math.isqrt(9)     # Retorna 3
math.isqrt(10)    # Retorna 3 (no redondea hacia arriba)
math.isqrt(25)    # Retorna 5

limite = math.isqrt(n)
for divisor in range(3, limite + 1, 2):
    ...
```

---

## Módulo `time`

### `time.time()`

**¿Qué realiza?**

Retorna el tiempo actual como un número de punto flotante que
representa los segundos transcurridos desde el epoch (1° de enero de
1970, UTC).

Se utiliza habitualmente para medir el tiempo de ejecución de un
fragmento de código: se registra el tiempo antes y después, y se
calcula la diferencia.

Requiere `import time`.

**¿Qué retorna?**

Un valor de tipo `float`.

**Ejemplos típicos:**

```python
import time

inicio = time.time()

# ... código a medir ...

fin = time.time()
print(f"Tiempo de ejecución: {fin - inicio} segundos")
```

---

## Construcciones del Lenguaje

Las siguientes construcciones no son funciones ni métodos, sino
características propias de la sintaxis y la semántica de Python que
aparecen con frecuencia en los ejercicios de este capítulo.

### Parámetros con valor por defecto

**¿Qué realiza?**

Permite definir funciones en las que algunos parámetros tienen un
valor predeterminado. Si el argumento no se proporciona en la llamada,
se usa el valor por defecto.

**Sintaxis:**

```python
def nombre_funcion(param1, param2=valor_defecto):
    ...
```

**Ejemplos típicos:**

```python
def calcular_precio(base, iva=21, descuento=0):
    con_iva = base * (1 + iva / 100)
    return con_iva * (1 - descuento / 100)

calcular_precio(1000)                      # iva=21, descuento=0
calcular_precio(1000, descuento=15)        # iva=21, descuento=15
calcular_precio(1000, iva=10.5, descuento=5)
```

Los parámetros con valor por defecto deben ubicarse después de los
parámetros sin valor por defecto.

### `**kwargs` — Argumentos de nombre arbitrario

**¿Qué realiza?**

Permite que una función reciba un número arbitrario de argumentos con
nombre. Dentro de la función, el parámetro definido con `**` es un
diccionario con los argumentos adicionales recibidos.

El nombre `kwargs` es una convención. Lo que define la construcción
es el doble asterisco `**`.

**Sintaxis:**

```python
def nombre_funcion(param1, param2, **kwargs):
    ...
```

**Ejemplos típicos:**

```python
def crear_ficha(nombre, edad, **datos_extra):
    ficha = {"nombre": nombre, "edad": edad}
    ficha.update(datos_extra)
    return ficha

ana = crear_ficha("Ana", 25, carrera="Ingeniería", ciudad="La Plata")
# datos_extra = {"carrera": "Ingeniería", "ciudad": "La Plata"}

juan = crear_ficha("Juan", 30)
# datos_extra = {}
```

Cuando no se pasan argumentos adicionales, `datos_extra` es un
diccionario vacío.

### `lambda` — Funciones anónimas

**¿Qué realiza?**

Crea una función anónima (sin nombre) de una sola expresión. Se
utiliza principalmente cuando se necesita una función pequeña como
argumento de otra función.

**Sintaxis:**

```python
lambda parámetros: expresión
```

**Ejemplos típicos:**

```python
lambda p: p[1]         # Retorna el segundo elemento de p
lambda par: par[1]     # Retorna el valor en la posición 1

doblar = lambda x: x * 2
doblar(5)              # Retorna 10
```

Las funciones `lambda` pueden recibir múltiples parámetros:

```python
lambda x, y: x + y    # Suma dos valores
```

Una función `lambda` es equivalente a una función `def` de una sola
línea con `return`:

```python
# Equivalentes:
lambda x: x * 2

def doblar(x):
    return x * 2
```

Se prefiere `lambda` cuando la función es corta y se usa una sola vez,
típicamente como argumento de otra función.

### `key=lambda` en `sorted()`, `max()` y `min()`

**¿Qué realiza?**

El parámetro `key` de funciones como `sorted()`, `max()` y `min()`
acepta una función que se aplica a cada elemento antes de realizar la
comparación. Cuando se combina con `lambda`, permite ordenar o comparar
según cualquier criterio sin modificar los elementos originales.

El resultado siempre contiene los elementos originales, no los valores
transformados por `key`.

**Ejemplos típicos:**

```python
productos = [("pan", 500, 20), ("leche", 800, 5), ("queso", 1200, 3)]

sorted(productos, key=lambda p: p[1])
# Ordena por precio (segundo elemento)

sorted(productos, key=lambda p: p[2])
# Ordena por stock (tercer elemento)

max(productos, key=lambda p: p[1])
# Retorna ("queso", 1200, 3), no 1200

notas = {"Ana": 8, "Juan": 6, "Pedro": 9}
sorted(notas.items(), key=lambda par: par[1], reverse=True)
# Ordena por nota de mayor a menor
```

### Retorno múltiple

**¿Qué realiza?**

Una función puede retornar más de un valor separándolos con comas.
Python los agrupa internamente en una tupla. Al recibir el resultado,
se puede desempaquetar en variables individuales.

**Ejemplos típicos:**

```python
def estadisticas(numeros):
    return sum(numeros), min(numeros), max(numeros)

# Desempaquetado en variables individuales
total, minimo, maximo = estadisticas([7, 3, 9, 5, 8])

# También puede recibirse como tupla
resultado = estadisticas([7, 3, 9, 5, 8])
print(resultado[0])   # total
```

`return a, b` es equivalente a `return (a, b)`. Al desempaquetar,
la cantidad de variables debe coincidir con la cantidad de valores
retornados.

### Docstrings

**¿Qué realiza?**

Una cadena de documentación (docstring) es un string literal que
aparece como primera sentencia en el cuerpo de una función, clase o
módulo. Sirve para documentar el propósito y el comportamiento del
objeto.

La función `help()` utiliza el docstring para mostrar la ayuda.

**Sintaxis:**

```python
def nombre_funcion(params):
    """Descripción breve de la función.

    Descripción detallada del comportamiento,
    parámetros y valores de retorno.
    """
    ...
```

**Ejemplos típicos:**

```python
def calcular_precio(base, iva=21, descuento=0):
    """Calcula el precio final aplicando IVA y luego descuento.

    base: precio sin impuestos
    iva: porcentaje de IVA (por defecto 21)
    descuento: porcentaje de descuento (por defecto 0)
    """
    con_iva = base * (1 + iva / 100)
    return con_iva * (1 - descuento / 100)

help(calcular_precio)   # Muestra el docstring
```

### Rebanada inversa `[::-1]`

**¿Qué realiza?**

La rebanada con paso `-1` recorre la secuencia de derecha a izquierda,
produciendo una copia invertida del string, lista o tupla.

**Sintaxis:**

```python
secuencia[::-1]
```

**Ejemplos típicos:**

```python
"Python"[::-1]              # Retorna "nohtyP"
"Anita lava la tina"        # Para verificar palíndromos:

def es_palindromo(texto):
    limpio = texto.lower().replace(" ", "")
    return limpio == limpio[::-1]

es_palindromo("Reconocer")  # True
```

### Rebanada `[:n]`

**¿Qué realiza?**

Extrae los primeros `n` elementos de una secuencia (string, lista,
tupla).

**Sintaxis:**

```python
secuencia[:n]
```

**Ejemplos típicos:**

```python
[10, 9, 8, 7, 6, 5][:3]          # Retorna [10, 9, 8]

sorted(lista, reverse=True)[:3]   # Los tres mayores elementos
sorted(lista, reverse=True)[:n]   # Los n mayores elementos
```

---

## Resumen por Categoría

| Categoría                       | Elementos                                                                                                    |
| ------------------------------- | ------------------------------------------------------------------------------------------------------------ |
| **Funciones built-in**          | `help`, `input`, `int`, `len`, `max`, `min`, `print`, `range`, `sorted`, `sum`                               |
| **Métodos de `str`**            | `center`, `isdigit`, `lower`, `replace`, `split`, `startswith`, `upper`                                      |
| **Métodos de `list`**           | `append`                                                                                                     |
| **Métodos de `dict`**           | `get`, `items`, `update`                                                                                     |
| **Módulo `math`**               | `isqrt`                                                                                                      |
| **Módulo `time`**               | `time`                                                                                                       |
| **Construcciones del lenguaje** | parámetros por defecto, `**kwargs`, `lambda`, `key=lambda`, retorno múltiple, docstrings, `[::-1]`, `[:n]`   |

---

## Notas Importantes

- **Funciones vs. métodos:** Las funciones built-in se invocan
  directamente, por ejemplo, `sorted(lista)` o `len(texto)`. Los
  métodos se invocan sobre un objeto, por ejemplo, `lista.append(x)` o
  `texto.lower()`.

- **Parámetros y argumentos:** Los *parámetros* son las variables en
  la definición de la función. Los *argumentos* son los valores que se
  pasan en la llamada.

```python
def suma(a, b):   # a y b son parámetros
    return a + b

suma(3, 5)        # 3 y 5 son argumentos
```

- **Argumentos por nombre en la llamada:** Python permite pasar
  argumentos por su nombre. Esto permite saltar parámetros con valor
  por defecto o cambiar el orden de los argumentos.

```python
calcular_precio(1000, descuento=15)
calcular_precio(1000, iva=10.5, descuento=5)
```

- **Alcance de variables (scope):** Las variables definidas dentro de
  una función son locales. No afectan a las variables del mismo nombre
  fuera de ella.

```python
def cambiar_valor(x):
    x = 999            # Solo modifica la variable local
    print(f"Adentro: {x}")

numero = 5
cambiar_valor(numero)
print(f"Afuera: {numero}")   # Sigue siendo 5
```

- **`**kwargs` como diccionario:** Dentro de la función, `datos_extra`
  (o el nombre que se elija) se comporta como un diccionario común.
  Puede iterarse, pasarse a `dict.update()`, o accederse por clave.

```python
def crear_ficha(nombre, **datos_extra):
    for clave, valor in datos_extra.items():
        print(f"{clave}: {valor}")
```

- **`key=` no modifica los elementos:** Cuando se usa `key=` en
  `sorted()`, `max()` o `min()`, la función `key` se usa solo para la
  comparación. El resultado contiene los elementos originales.

```python
productos = [("pan", 500), ("leche", 800)]
max(productos, key=lambda p: p[1])
# Retorna ("leche", 800), no 800
```

- **`sorted()` vs. `list.sort()`:** `sorted()` retorna una nueva lista
  y no modifica el original. `list.sort()` modifica la lista en el
  lugar y retorna `None`. En estos ejercicios se utiliza `sorted()`.

```python
numeros = [3, 1, 4]

ordenados = sorted(numeros)   # numeros no cambia
numeros.sort()                # numeros cambia, retorna None
```

- **Retorno múltiple y tuplas:** `return a, b` es equivalente a
  `return (a, b)`. Al desempaquetar, la cantidad de variables debe
  coincidir con la cantidad de valores retornados.

```python
def minmax(nums):
    return min(nums), max(nums)

mi, ma = minmax([3, 1, 9])     # Desempaquetado correcto
resultado = minmax([3, 1, 9])  # resultado es una tupla
```

- **Docstrings y `help()`:** El docstring se escribe con triple
  comilla `"""` inmediatamente después de `def`. No es un comentario;
  es un string que Python almacena como atributo de la función y que
  `help()` puede mostrar.

- **`math.isqrt()` para primos:** Al verificar si `n` es primo,
  alcanza con buscar divisores hasta `√n`. Usar `math.isqrt(n)` en
  lugar de `int(n ** 0.5)` garantiza el resultado entero exacto sin
  errores de punto flotante.

- **PEP 8:** PEP 8 es la guía de estilo para código Python. Entre sus
  recomendaciones se encuentra limitar a 79 caracteres las líneas de
  código y a 72 caracteres las líneas de comentarios y docstrings.
  Estas recomendaciones corresponden al código Python y no constituyen
  una regla obligatoria para los archivos Markdown.
