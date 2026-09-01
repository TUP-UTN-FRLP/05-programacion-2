# Funciones Utilizadas en capitulo_07_Comprehensions

Documento que agrupa las funciones built-in, los métodos y las
construcciones del lenguaje utilizados en los ejercicios y enunciados,
organizados por tipo y en orden alfabético.

---

## Funciones Generales

### `abs(número)`

**¿Qué realiza?**

Retorna el valor absoluto de un número. Si el número es negativo,
lo convierte en positivo. Si ya es positivo o cero, lo retorna sin
cambios.

**¿Qué retorna?**

Un número del mismo tipo que el argumento (`int` o `float`).

**Ejemplos típicos:**

```python
abs(-5)      # Retorna 5
abs(3)       # Retorna 3
abs(-2.7)    # Retorna 2.7

absolutos = [abs(n) for n in numeros]
```

### `enumerate(iterable)`

**¿Qué realiza?**

Recorre un iterable y genera pares `(índice, elemento)` para cada
posición. El índice empieza desde `0` por defecto.

Se utiliza cuando, además del valor de cada elemento, se necesita
conocer su posición dentro de la secuencia.

**¿Qué retorna?**

Un objeto `enumerate` iterable, donde cada elemento es una tupla
`(índice, valor)`.

**Ejemplos típicos:**

```python
enumerate("hola")
# Genera: (0, "h"), (1, "o"), (2, "l"), (3, "a")

posiciones = [i for i, letra in enumerate(texto) if letra == "a"]
# Desempaquetado: i recibe el índice, letra recibe el carácter
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
texto = input("Texto: ")    # Retorna un str
frase = input("Frase: ")    # Retorna un str
```

### `len(colección)`

**¿Qué realiza?**

Retorna la cantidad de elementos de una colección o la longitud de un
string.

Funciona con listas, tuplas, sets, diccionarios, strings y cualquier
objeto que implemente la interfaz de secuencia o colección.

**¿Qué retorna?**

Un valor de tipo `int`.

**Ejemplos típicos:**

```python
len([1, 2, 3])       # Retorna 3
len("Hola")          # Retorna 4
len({})              # Retorna 0

promedio = sum(p for p in precios) / len(precios)
print(f"Hay {len(letras)} letras en total")
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
print(multiplos)
print(f"La 'a' aparece en las posiciones: {posiciones}")
print(f"Total: ${total}")
print(f"Promedio: ${promedio:.2f}")
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
range(1, 21)    # 1, 2, 3, ..., 20
range(1, 11)    # 1, 2, 3, ..., 10

multiplos = [n * 5 for n in range(1, 21)]
triples = [n * 3 for n in range(1, 11)]
```

### `round(número, decimales)`

**¿Qué realiza?**

Redondea un número de punto flotante al número de decimales indicado.
Si se omite el segundo argumento, redondea al entero más cercano.

**¿Qué retorna?**

Un `float` si se especifican decimales, un `int` si se omite el
segundo argumento.

**Ejemplos típicos:**

```python
round(3.14159, 2)     # Retorna 3.14
round(500 / 1000, 2)  # Retorna 0.5

en_dolares = {p: round(precio / 1000, 2) for p, precio in precios.items()}
```

### `set(iterable)`

**¿Qué realiza?**

Convierte un iterable en un `set`, eliminando los elementos
duplicados. El resultado no tiene un orden garantizado.

Se diferencia de la comprensión de conjunto en que recibe un iterable
ya construido en lugar de definir la lógica de generación inline.

**¿Qué retorna?**

Un objeto de tipo `set`.

**Ejemplos típicos:**

```python
set([1, 2, 2, 3])              # Retorna {1, 2, 3}
set("hola")                    # Retorna {'h', 'o', 'l', 'a'}
set(texto.lower().split())     # Palabras únicas normalizadas
```

### `sum(iterable)`

**¿Qué realiza?**

Retorna la suma de los elementos de un iterable numérico.

En este capítulo se utiliza de forma especial con expresiones
generadoras, tanto para sumar valores numéricos como para contar
elementos que cumplen una condición (aprovechando que `True == 1` y
`False == 0`).

**¿Qué retorna?**

La suma total. El tipo del resultado depende de los elementos del
iterable.

**Ejemplos típicos:**

```python
sum([1, 2, 3, 4])                            # Retorna 10

total = sum(p for p in precios)
promedio = sum(p for p in precios) / len(precios)

# Contar elementos con una condición (True == 1, False == 0)
caros = sum(p > 1000 for p in precios)

# Suma de una expresión compuesta
total = sum(datos["precio"] * datos["stock"] for datos in catalogo.values())
```

### `zip(iter1, iter2, ...)`

**¿Qué realiza?**

Combina dos o más iterables elemento a elemento, generando tuplas con
un elemento de cada uno. Se detiene cuando el iterable más corto se
agota.

**¿Qué retorna?**

Un objeto `zip` iterable, donde cada elemento es una tupla con un
valor de cada iterable.

**Ejemplos típicos:**

```python
zip(["Ana", "Juan"], [8, 6])
# Genera: ("Ana", 8), ("Juan", 6)

reporte = [f"{n}: {nota}" for n, nota in zip(nombres, notas)]
# Desempaquetado: n recibe el nombre, nota recibe la calificación
```

---

## Métodos de Strings (Cadenas de Texto)

Los siguientes elementos son métodos de la clase `str`. Se invocan
sobre un objeto de tipo string, por ejemplo, `texto.lower()`.

### `string.isalpha()`

**¿Qué realiza?**

Verifica si todos los caracteres del string son letras del alfabeto.
Los espacios, signos de puntuación, dígitos y símbolos no se
consideran letras.

**¿Qué retorna?**

`True` si el string no está vacío y todos sus caracteres son letras.
`False` en caso contrario.

**Ejemplos típicos:**

```python
"Hola".isalpha()     # Retorna True
"Ana".isalpha()      # Retorna True
"123".isalpha()      # Retorna False
"a b".isalpha()      # Retorna False (el espacio no es letra)
"a!".isalpha()       # Retorna False

letras = {c for c in frase if c.isalpha()}
# Filtra solo las letras, descartando espacios y signos
```

### `string.lower()`

**¿Qué realiza?**

Devuelve una versión del string en la que los caracteres que tienen
una correspondencia en minúscula se convierten a minúsculas.

**¿Qué retorna?**

Un nuevo string. El string original no se modifica porque los strings
de Python son inmutables.

**Ejemplos típicos:**

```python
"PYTHON".lower()                         # Retorna "python"
"Hola Mundo".lower()                     # Retorna "hola mundo"

enumerate(texto.lower())                 # Itera con letras en minúsculas
set(texto.lower().split())               # Palabras únicas normalizadas
{p for p in palabras if p[0].lower() in "aeiouáéíóú"}
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

texto.lower().split()         # Palabras normalizadas a minúsculas
{palabra for palabra in frase.split()}
```

### `string.upper()`

**¿Qué realiza?**

Devuelve una versión del string en la que los caracteres que tienen
una correspondencia en mayúscula se convierten a mayúsculas.

**¿Qué retorna?**

Un nuevo string. El string original no se modifica porque los strings
de Python son inmutables.

**Ejemplos típicos:**

```python
"python".upper()                 # Retorna "PYTHON"
"hola mundo".upper()             # Retorna "HOLA MUNDO"

mayus = [p.upper() for p in palabras]
```

---

## Métodos de Listas

Los siguientes elementos son métodos de la clase `list`. Se invocan
sobre un objeto de tipo lista, por ejemplo, `mi_lista.count(x)`.

### `list.count(valor)`

**¿Qué realiza?**

Cuenta cuántas veces aparece `valor` en la lista.

**¿Qué retorna?**

Un valor de tipo `int` con la cantidad de ocurrencias.

**Ejemplos típicos:**

```python
[1, 2, 2, 3, 2].count(2)    # Retorna 3
[7, 3, 3, 5].count(3)       # Retorna 2
[7, 3, 3, 5].count(9)       # Retorna 0

repetidos = {n for n in numeros if numeros.count(n) > 1}
# Incluye solo los números que aparecen más de una vez
```

---

## Métodos de Diccionarios

Los siguientes elementos son métodos de la clase `dict`. Se invocan
sobre un objeto de tipo diccionario.

### `dict.items()`

**¿Qué realiza?**

Retorna una vista de los pares clave-valor del diccionario, como una
secuencia de tuplas `(clave, valor)`.

**¿Qué retorna?**

Un objeto `dict_items`. Es iterable y refleja el estado actual del
diccionario.

**Ejemplos típicos:**

```python
precios = {"pan": 500, "leche": 800}

for producto, precio in precios.items():
    print(producto, precio)

en_dolares = {p: round(precio / 1000, 2) for p, precio in precios.items()}
aprobados = {nombre: nota for nombre, nota in notas.items() if nota >= 7}
invertido = {v: k for k, v in original.items()}
```

### `dict.values()`

**¿Qué realiza?**

Retorna una vista de todos los valores del diccionario.

**¿Qué retorna?**

Un objeto `dict_values`. Es iterable y refleja el estado actual del
diccionario.

**Ejemplos típicos:**

```python
catalogo = {"pan": {"precio": 500, "stock": 20}, ...}

sum(datos["precio"] * datos["stock"] for datos in catalogo.values())

alumnos = {"Ana": {"Matemática": 8, "Programación": 9}, ...}
{nombre: sum(materias.values()) / len(materias) for nombre, materias in alumnos.items()}
```

---

## Construcciones del Lenguaje

Las siguientes construcciones no son funciones ni métodos, sino
características propias de la sintaxis y la semántica de Python que
son el tema central de este capítulo.

### Comprensión de lista `[expresión for var in iterable]`

**¿Qué realiza?**

Genera una nueva lista aplicando una expresión a cada elemento de
un iterable. Es equivalente a un bucle `for` que agrega elementos a
una lista con `append()`, pero más concisa y, en general, más
eficiente.

**Sintaxis:**

```python
[expresión for variable in iterable]
```

**Ejemplos típicos:**

```python
multiplos = [n * 5 for n in range(1, 21)]
triples = [n * 3 for n in range(1, 11)]
absolutos = [abs(n) for n in numeros]
mayus = [p.upper() for p in palabras]
```

### Comprensión de lista con filtro `[expresión for var in iterable if condición]`

**¿Qué realiza?**

Igual que la comprensión de lista, pero incluye solo los elementos
para los que la condición es `True`.

**Sintaxis:**

```python
[expresión for variable in iterable if condición]
```

**Ejemplos típicos:**

```python
grandes = [n for n in numeros if n > 20]
con_iva = [p * 1.21 for p in precios if p > 1000]
divisibles = [n for n in range(1, 21) if n % 3 == 0 or n % 5 == 0]
posiciones = [i for i, letra in enumerate(texto.lower()) if letra == "a"]
disponibles = [producto for producto, datos in catalogo.items()
               if datos["stock"] > 0]
```

### Comprensión de diccionario `{clave: valor for var in iterable}`

**¿Qué realiza?**

Genera un nuevo diccionario a partir de un iterable. La parte
izquierda de los dos puntos define la clave y la derecha el valor.

**Sintaxis:**

```python
{expresión_clave: expresión_valor for variable in iterable}
```

**Ejemplos típicos:**

```python
en_dolares = {producto: round(precio / 1000, 2)
              for producto, precio in precios.items()}

invertido = {v: k for k, v in original.items()}

longitudes = {palabra: len(palabra) for palabra in set(texto.lower().split())}

longitudes = {len(n): n for n in nombres}
```

### Comprensión de diccionario con filtro

**¿Qué realiza?**

Igual que la comprensión de diccionario, pero incluye solo los pares
clave-valor para los que la condición es `True`.

**Sintaxis:**

```python
{expr_clave: expr_valor for variable in iterable if condición}
```

**Ejemplos típicos:**

```python
aprobados = {nombre: nota for nombre, nota in notas.items() if nota >= 7}

promedios = {
    nombre: sum(materias.values()) / len(materias)
    for nombre, materias in alumnos.items()
}
```

### Comprensión de conjunto `{expresión for var in iterable}`

**¿Qué realiza?**

Genera un nuevo `set` a partir de un iterable. Al igual que todos
los sets, el resultado no contiene duplicados y no tiene un orden
garantizado.

Se distingue de la comprensión de diccionario por no tener los dos
puntos `clave: valor`; solo tiene una expresión.

**Sintaxis:**

```python
{expresión for variable in iterable}
```

**Ejemplos típicos:**

```python
unicas = {palabra for palabra in frase.split()}
letras = {c for c in frase if c.isalpha()}
```

### Comprensión de conjunto con filtro

**¿Qué realiza?**

Igual que la comprensión de conjunto, pero incluye solo los elementos
para los que la condición es `True`.

**Sintaxis:**

```python
{expresión for variable in iterable if condición}
```

**Ejemplos típicos:**

```python
con_vocal = {p for p in palabras if p[0].lower() in "aeiouáéíóú"}
repetidos = {n for n in numeros if numeros.count(n) > 1}
```

### Expresión generadora `(expresión for var in iterable)`

**¿Qué realiza?**

Genera los valores uno por uno, sin construir una colección completa
en memoria. Su sintaxis es igual a la comprensión de lista pero usa
paréntesis en lugar de corchetes.

Se utiliza principalmente como argumento directo de funciones como
`sum()` o `max()`, lo que hace que los valores se calculen
y consuman de inmediato, sin necesitar almacenarlos.

**Sintaxis:**

```python
(expresión for variable in iterable)
```

Cuando se pasa como único argumento a una función, los paréntesis
del generador y los de la llamada pueden fundirse en uno solo:

```python
sum(expresión for variable in iterable)
# Equivalente a:
sum((expresión for variable in iterable))
```

**Ejemplos típicos:**

```python
total = sum(p for p in precios)
promedio = sum(p for p in precios) / len(precios)

# Generar booleans y sumar (True == 1, False == 0)
caros = sum(p > 1000 for p in precios)

total = sum(datos["precio"] * datos["stock"] for datos in catalogo.values())
```

### Comprensión anidada `[expr for var1 in iter1 for var2 in iter2]`

**¿Qué realiza?**

Recorre múltiples iterables mediante varios `for` encadenados dentro
de una misma comprensión. Cada `for` adicional es como un bucle
interno: por cada elemento del primero, se recorre el segundo
completo.

Se utiliza para aplanar estructuras de listas de listas (matrices)
o para generar combinaciones.

**Sintaxis:**

```python
[expresión for var1 in iterable1 for var2 in iterable2]
```

El orden de los `for` es el mismo que en los bucles anidados:
el primero es el externo y el segundo es el interno.

**Ejemplos típicos:**

```python
matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]

# Aplana la matriz: recorre filas y, por cada fila, cada elemento
aplanada = [x for fila in matriz for x in fila]
# Retorna [1, 2, 3, 4, 5, 6, 7, 8, 9]

# Con filtro adicional
pares = [x for fila in matriz for x in fila if x % 2 == 0]
# Retorna [2, 4, 6, 8]
```

```python
# Equivalente con bucles anidados:
aplanada = []
for fila in matriz:
    for x in fila:
        aplanada.append(x)
```

### Expresión condicional inline `valor_si_true if condición else valor_si_false`

**¿Qué realiza?**

Permite escribir una elección entre dos valores en una sola expresión.
Se evalúa la condición: si es `True` se usa el primer valor; si es
`False` se usa el valor después de `else`.

Se diferencia del filtro `if` de las comprensiones en que no descarta
elementos: todos se incluyen, pero con un valor diferente según la
condición.

**Sintaxis:**

```python
valor_si_verdadero if condición else valor_si_falso
```

**Ejemplos típicos:**

```python
"par" if n % 2 == 0 else "impar"

clasificados = [(n, "par" if n % 2 == 0 else "impar") for n in numeros]
# Todos los números se incluyen; cada uno va acompañado de su clasificación
```

### Desempaquetado de tuplas en `for`

**¿Qué realiza?**

Cuando se itera sobre un iterable de tuplas (como `zip()`,
`enumerate()` o `dict.items()`), es posible asignar cada elemento
de la tupla a variables separadas directamente en el `for`.

Esta técnica se llama *desempaquetado* y evita tener que acceder a
los elementos por índice (`par[0]`, `par[1]`).

**Sintaxis:**

```python
for var1, var2 in iterable_de_tuplas:
    ...
```

**Ejemplos típicos:**

```python
# Con zip(): itera pares (nombre, nota)
reporte = [f"{n}: {nota}" for n, nota in zip(nombres, notas)]

# Con enumerate(): itera pares (índice, carácter)
posiciones = [i for i, letra in enumerate(texto.lower()) if letra == "a"]

# Con dict.items(): itera pares (clave, valor)
aprobados = {nombre: nota for nombre, nota in notas.items() if nota >= 7}

# Con dict.items() anidado: desempaqueta dos niveles
{nombre: sum(materias.values()) / len(materias)
 for nombre, materias in alumnos.items()}
```

### f-strings (cadenas formateadas)

**¿Qué realiza?**

Permiten incrustar expresiones de Python directamente dentro de un
string. Se escriben con el prefijo `f` y las expresiones se colocan
entre llaves `{}`.

**Sintaxis:**

```python
f"texto {expresión} texto"
f"número con decimales {valor:.2f}"
```

**Ejemplos típicos:**

```python
print(f"La 'a' aparece en las posiciones: {posiciones}")
print(f"Total: ${total}")
print(f"Promedio: ${promedio:.2f}")
print(f"Precios sobre $1000: {caros}")
print(f"Valor total del inventario: ${total}")
print(f"Hay {len(letras)} letras en total")
print(f"{nombre}: {promedio:.2f}")
```

---

## Resumen por Categoría

| Categoría                       | Elementos                                                                                                                                                                                    |
| ------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Funciones built-in**          | `abs`, `enumerate`, `input`, `len`, `print`, `range`, `round`, `set`, `sum`, `zip`                                                                                                           |
| **Métodos de `str`**            | `isalpha`, `lower`, `split`, `upper`                                                                                                                                                         |
| **Métodos de `list`**           | `count`                                                                                                                                                                                      |
| **Métodos de `dict`**           | `items`, `values`                                                                                                                                                                            |
| **Construcciones del lenguaje** | comprensión de lista, comprensión de lista con filtro, comprensión de diccionario, comprensión de diccionario con filtro, comprensión de conjunto, comprensión de conjunto con filtro, comprensión anidada, expresión condicional inline, desempaquetado de tuplas en `for`, f-strings                                                                                                            |

---

## Notas Importantes

- **Cuatro tipos de comprensiones:** Python tiene comprensiones para
  listas `[...]`, diccionarios `{clave: valor ...}`, sets `{expr ...}`
  y generadores `(...)`. La forma de distinguirlas es por los
  delimitadores y la presencia o ausencia de los dos puntos `clave:
  valor`.

- **Filtro vs. expresión condicional:** El `if` al final de la
  comprensión descarta elementos. La expresión condicional
  `a if cond else b` transforma elementos sin descartarlos. Ambos
  pueden combinarse:

```python
# Solo con filtro: descarta los negativos
positivos = [n for n in numeros if n > 0]

# Solo con expresión condicional: clasifica todos
signos = ["pos" if n > 0 else "neg" for n in numeros]

# Combinados: clasifica solo los que no son cero
signos = ["pos" if n > 0 else "neg" for n in numeros if n != 0]
```

- **Generadores dentro de `sum()`:** No es necesario construir una
  lista completa para calcular una suma. Pasar una expresión generadora
  directamente a `sum()` es más eficiente en memoria:

```python
# Con lista (construye toda la lista primero):
total = sum([p for p in precios])

# Con generador (calcula uno a uno):
total = sum(p for p in precios)
```

- **Contar con `sum()` y booleanos:** Aprovechar que `True == 1` y
  `False == 0` permite contar elementos que cumplen una condición sin
  necesidad de un filtro explícito:

```python
caros = sum(p > 1000 for p in precios)
# Cuenta cuántos precios superan $1000
```

- **Comprensión anidada y orden de los `for`:** El orden de los `for`
  en una comprensión anidada es el mismo que en los bucles anidados:
  el primero es el externo (la fila) y el segundo es el interno (el
  elemento dentro de la fila).

```python
[x for fila in matriz for x in fila]
# fila es el bucle externo: recorre cada sublista
# x es el bucle interno: recorre cada elemento de esa sublista
```

- **`dict.items()` con desempaquetado:** Al iterar sobre
  `diccionario.items()`, cada elemento es una tupla `(clave, valor)`.
  Desempaquetar en el `for` hace el código más legible que acceder por
  índice:

```python
# Sin desempaquetar (menos legible):
for par in notas.items():
    print(par[0], par[1])

# Con desempaquetar (más legible):
for nombre, nota in notas.items():
    print(nombre, nota)
```

- **`set()` vs. comprensión de conjunto:** Ambos producen un `set`,
  pero se usan en contextos distintos. `set(iterable)` convierte algo
  ya construido; la comprensión de conjunto `{expr for ...}` define
  la lógica de generación inline:

```python
set(texto.split())             # Convierte una lista ya creada
{p for p in texto.split()}     # Define la lógica dentro de la comprensión
```

- **`enumerate()` para índices:** En comprensiones, `enumerate()`
  es la forma idiomática de obtener tanto el índice como el valor
  de cada elemento. Evita recurrir a un contador manual o a
  `range(len(...))`:

```python
# Forma no idiomática:
[i for i in range(len(texto)) if texto[i] == "a"]

# Forma idiomática con enumerate():
[i for i, letra in enumerate(texto) if letra == "a"]
```

- **`zip()` para combinar listas:** `zip()` es la forma idiomática
  de iterar en paralelo sobre dos o más listas. Combinado con el
  desempaquetado, evita acceder por índice:

```python
# Forma no idiomática:
[f"{nombres[i]}: {notas[i]}" for i in range(len(nombres))]

# Forma idiomática con zip():
[f"{n}: {nota}" for n, nota in zip(nombres, notas)]
```
