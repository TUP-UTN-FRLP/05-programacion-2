# Funciones utilizadas en Colecciones

Documento de referencia que reúne funciones incorporadas (built-in) y métodos utilizados para trabajar con colecciones y strings.

Los elementos están organizados por categoría y, dentro de cada categoría, en orden alfabético.

---

## Funciones y tipos generales

### `all(iterable)`

**¿Qué realiza?**
Verifica si todos los elementos de un iterable son verdaderos según las reglas de evaluación booleana de Python.

**¿Qué retorna?**
`True` si todos los elementos son verdaderos y `False` si al menos uno es falso.

Un iterable vacío produce `True`.

**Ejemplos:**

```python
all([True, True, True])
# True

all([True, False, True])
# False

all([1, 2, 3])
# True

all([1, 0, 3])
# False

all([])
# True

notas = [8, 7, 9, 6]
all(nota >= 6 for nota in notas)
# True
```

### `any(iterable)`

**¿Qué realiza?**
Verifica si al menos uno de los elementos de un iterable es verdadero según las reglas de evaluación booleana de Python.

**¿Qué retorna?**
`True` si al menos un elemento es verdadero y `False` si todos son falsos.

Un iterable vacío produce `False`.

**Ejemplos:**

```python
any([False, False, True])
# True

any([False, False, False])
# False

any([0, 0, 5])
# True

any([0, False, ""])
# False

any([])
# False

notas = [4, 5, 8, 3]
any(nota >= 6 for nota in notas)
# True
```

### `dict(iterable)` o `dict(**argumentos)`

**¿Qué realiza?**
Crea un nuevo diccionario.

Puede recibir, entre otras posibilidades, un iterable de pares clave-valor o argumentos con nombre.

**¿Qué retorna?**
Un objeto de tipo `dict`.

**Ejemplos:**

```python
dict()
# {}

dict(nombre="Ana", edad=20)
# {'nombre': 'Ana', 'edad': 20}

dict([("nombre", "Ana"), ("edad", 20)])
# {'nombre': 'Ana', 'edad': 20}
```

### `enumerate(iterable, start=0)`

**¿Qué realiza?**
Permite recorrer un iterable obteniendo simultáneamente un contador y cada elemento.

**¿Qué retorna?**
Un objeto `enumerate`.

Cada elemento producido es una tupla formada por:

```text
(índice, elemento)
```

El contador comienza en `0` por defecto.

**Ejemplo:**

```python
nombres = ["Ana", "Juan", "Lucía"]

for i, nombre in enumerate(nombres):
    print(i, nombre)

# Salida:
# 0 Ana
# 1 Juan
# 2 Lucía
```

El valor inicial puede modificarse:

```python
for i, nombre in enumerate(nombres, start=1):
    print(i, nombre)

# Salida:
# 1 Ana
# 2 Juan
# 3 Lucía
```

Puede convertirse a una lista:

```python
list(enumerate(["a", "b", "c"]))
# [(0, 'a'), (1, 'b'), (2, 'c')]
```

### `float(valor)`

**¿Qué realiza?**
Convierte un valor compatible en un número de punto flotante (`float`).

**¿Qué retorna?**
Un objeto de tipo `float`.

**Ejemplos:**

```python
float("3.14")
# 3.14

float(5)
# 5.0

precio = float(input("Precio: "))
```

### `input(mensaje)`

**¿Qué realiza?**
Muestra un mensaje y espera que el usuario introduzca un valor mediante la entrada estándar.

**¿Qué retorna?**
Siempre retorna un string (`str`), independientemente de lo que escriba el usuario.

**Ejemplo:**

```python
nombre = input("¿Cuál es tu nombre? ")
```

Si el usuario escribe:

```text
Juan
```

entonces:

```python
nombre
# "Juan"
```

Para convertir la entrada:

```python
edad = int(input("Edad: "))
precio = float(input("Precio: "))
```

### `int(valor)`

**¿Qué realiza?**
Convierte un valor compatible en un número entero (`int`).

Cuando recibe un número de punto flotante, elimina la parte fraccionaria hacia cero.

**¿Qué retorna?**
Un objeto de tipo `int`.

**Ejemplos:**

```python
int("42")
# 42

int(3.14)
# 3

int(-3.14)
# -3

edad = int(input("Edad: "))
```

La división entera mediante `//` es una operación diferente:

```python
47 // 5
# 9
```

### `len(objeto)`

**¿Qué realiza?**
Obtiene la cantidad de elementos de un objeto que define una longitud.

Puede utilizarse, entre otros, con strings, listas, tuplas, diccionarios, sets y `range`.

En un diccionario, cuenta sus claves.

**¿Qué retorna?**
Un número entero (`int`).

**Ejemplos:**

```python
len([10, 20, 30])
# 3

len("Python")
# 6

len((10, 20))
# 2

len({"a": 1, "b": 2})
# 2

len({1, 2, 3})
# 3

len(range(10))
# 10
```

### `list(iterable)`

**¿Qué realiza?**
Crea una nueva lista a partir de un iterable.

Sin argumentos, crea una lista vacía.

**¿Qué retorna?**
Un objeto de tipo `list`.

**Ejemplos:**

```python
list()
# []

list("abc")
# ['a', 'b', 'c']

list((1, 2, 3))
# [1, 2, 3]

list(range(5))
# [0, 1, 2, 3, 4]
```

También permite convertir objetos iterables, como `dict_items`, `dict_values`, `enumerate` o `zip`, en listas:

```python
list(zip([1, 2], ["a", "b"]))
# [(1, 'a'), (2, 'b')]
```

### `max(iterable)` o `max(a, b, c, ...)`

**¿Qué realiza?**
Obtiene el elemento de mayor valor de un iterable o el mayor de los argumentos proporcionados.

**¿Qué retorna?**
El elemento de mayor valor.

**Ejemplos:**

```python
max([3, 1, 4, 1, 5])
# 5

max(10, 20, 5)
# 20

max("abc")
# 'c'

max(["Ana", "Juan", "Zoe"])
# 'Zoe'
```

En strings, la comparación se realiza según las reglas de comparación de strings de Python.

### `min(iterable)` o `min(a, b, c, ...)`

**¿Qué realiza?**
Obtiene el elemento de menor valor de un iterable o el menor de los argumentos proporcionados.

**¿Qué retorna?**
El elemento de menor valor.

**Ejemplos:**

```python
min([3, 1, 4, 1, 5])
# 1

min(10, 20, 5)
# 5

min("abc")
# 'a'
```

### `print(*objetos, sep=" ", end="\n")`

**¿Qué realiza?**
Escribe uno o más valores en la salida estándar, normalmente la consola.

`sep` permite indicar el separador entre los valores y `end` permite indicar qué se escribe al finalizar.

**¿Qué retorna?**
`None`.

**Ejemplos:**

```python
print("Hola")
# Hola

print(42)
# 42

print("Nombre:", "Juan")
# Nombre: Juan

print(1, 2, 3, sep="-")
# 1-2-3
```

### `range(stop)`

### `range(start, stop)`

### `range(start, stop, step)`

**¿Qué realiza?**
Representa una progresión de números enteros.

El valor `stop` no se incluye.

**¿Qué retorna?**
Un objeto de tipo `range`, no una lista.

**Ejemplos:**

```python
list(range(5))
# [0, 1, 2, 3, 4]

list(range(1, 6))
# [1, 2, 3, 4, 5]

list(range(0, 10, 2))
# [0, 2, 4, 6, 8]

list(range(5, 0, -1))
# [5, 4, 3, 2, 1]
```

### `set(iterable)`

**¿Qué realiza?**
Crea un nuevo conjunto a partir de un iterable.

Los conjuntos no contienen elementos duplicados.

**¿Qué retorna?**
Un objeto de tipo `set`.

**Ejemplos:**

```python
set()
# set()

set([1, 2, 2, 3])
# {1, 2, 3}

set("banana")
# {'b', 'a', 'n'}
```

El orden mostrado al representar un `set` no debe considerarse significativo.

### `sorted(iterable, reverse=False)`

**¿Qué realiza?**
Obtiene los elementos de un iterable y los ordena.

**¿Qué retorna?**
Una nueva lista con los elementos ordenados.

No modifica el objeto original.

**Ejemplos:**

```python
sorted([3, 1, 4, 1, 5])
# [1, 1, 3, 4, 5]

sorted([3, 1, 4], reverse=True)
# [4, 3, 1]

sorted("python")
# ['h', 'n', 'o', 'p', 't', 'y']

sorted({3, 1, 2})
# [1, 2, 3]
```

### `sum(iterable, start=0)`

**¿Qué realiza?**
Suma los elementos de un iterable comenzando desde el valor indicado por `start`.

Por defecto, `start` es `0`.

**¿Qué retorna?**
El resultado de la suma.

**Ejemplos:**

```python
sum([1, 2, 3, 4])
# 10

sum([1.5, 2.5, 3.0])
# 7.0

sum(range(1, 6))
# 15

sum([1, 2, 3], 10)
# 16
```

### `tuple(iterable)`

**¿Qué realiza?**
Crea una nueva tupla a partir de un iterable.

Sin argumentos, crea una tupla vacía.

**¿Qué retorna?**
Un objeto de tipo `tuple`.

**Ejemplos:**

```python
tuple()
# ()

tuple([1, 2, 3])
# (1, 2, 3)

tuple("abc")
# ('a', 'b', 'c')

tuple(range(3))
# (0, 1, 2)
```

Las tuplas son secuencias inmutables.

### `zip(iterable1, iterable2, ...)`

**¿Qué realiza?**
Combina elementos correspondientes de dos o más iterables.

Cada elemento producido es una tupla.

El recorrido finaliza cuando se alcanza el iterable más corto.

**¿Qué retorna?**
Un objeto de tipo `zip`.

**Ejemplo:**

```python
numeros = [1, 2, 3]
letras = ["a", "b", "c"]

list(zip(numeros, letras))
# [(1, 'a'), (2, 'b'), (3, 'c')]
```

También puede recorrerse directamente:

```python
for numero, letra in zip([1, 2, 3], ["a", "b", "c"]):
    print(numero, letra)

# Salida:
# 1 a
# 2 b
# 3 c
```

Si las longitudes son diferentes:

```python
list(zip([1, 2, 3], ["a", "b"]))
# [(1, 'a'), (2, 'b')]
```

---

## Métodos para strings

En los siguientes ejemplos, `string` representa genéricamente un objeto de tipo `str`.

### `string.isalnum()`

**¿Qué realiza?**
Verifica si todos los caracteres del string son alfanuméricos.

El string debe contener al menos un carácter.

**¿Qué retorna?**
`True` si todos los caracteres son alfanuméricos y `False` en caso contrario.

**Ejemplos:**

```python
"ABC".isalnum()
# True

"123".isalnum()
# True

"ABC123".isalnum()
# True

"ABC 123".isalnum()
# False

"ABC-123".isalnum()
# False
```

### `string.isalpha()`

**¿Qué realiza?**
Verifica si todos los caracteres del string son alfabéticos.

El string debe contener al menos un carácter.

**¿Qué retorna?**
`True` si todos los caracteres son alfabéticos y `False` en caso contrario.

**Ejemplos:**

```python
"abc".isalpha()
# True

"Python".isalpha()
# True

"Árbol".isalpha()
# True

"abc123".isalpha()
# False

"hola mundo".isalpha()
# False

"".isalpha()
# False
```

### `string.isdecimal()`

**¿Qué realiza?**
Verifica si todos los caracteres del string son caracteres decimales según Unicode.

El string debe contener al menos un carácter.

**¿Qué retorna?**
`True` si todos los caracteres son decimales y `False` en caso contrario.

**Ejemplos:**

```python
"123".isdecimal()
# True

"12.3".isdecimal()
# False

"-123".isdecimal()
# False

"123a".isdecimal()
# False

"".isdecimal()
# False
```

### `string.isdigit()`

**¿Qué realiza?**
Verifica si todos los caracteres del string son caracteres reconocidos como dígitos según Unicode.

El string debe contener al menos un carácter.

**¿Qué retorna?**
`True` si todos los caracteres son dígitos y `False` en caso contrario.

**Ejemplos:**

```python
"123".isdigit()
# True

"12.3".isdigit()
# False

"-123".isdigit()
# False

"abc".isdigit()
# False

"".isdigit()
# False

"²".isdigit()
# True
```

`isdigit()` analiza los caracteres del string. No comprueba si un valor numérico está dentro de un rango.

### `string.isnumeric()`

**¿Qué realiza?**
Verifica si todos los caracteres del string son caracteres numéricos según Unicode.

Es el método más amplio de los tres: `isdecimal()`, `isdigit()` e `isnumeric()`.

**¿Qué retorna?**
`True` si todos los caracteres son numéricos y `False` en caso contrario.

**Ejemplos:**

```python
"123".isnumeric()
# True

"²".isnumeric()
# True

"⅕".isnumeric()
# True

"12.3".isnumeric()
# False

"-123".isnumeric()
# False
```

### Relación entre `isdecimal()`, `isdigit()` e `isnumeric()`

De forma simplificada, existe una relación de inclusión:

```text
isdecimal() ⊂ isdigit() ⊂ isnumeric()
```

Por ejemplo:

```python
"5".isdecimal(), "5".isdigit(), "5".isnumeric()
# (True, True, True)

"²".isdecimal(), "²".isdigit(), "²".isnumeric()
# (False, True, True)

"⅕".isdecimal(), "⅕".isdigit(), "⅕".isnumeric()
# (False, False, True)
```

Estos métodos analizan caracteres. No equivalen a comprobar si un texto puede convertirse directamente mediante `int()` o `float()`.

Por ejemplo:

```python
"-12".isdigit()
# False

"12.5".isdigit()
# False
```

El signo `-` y el punto `.` no son caracteres reconocidos por `isdigit()`.

| String   | `isdecimal()` | `isdigit()` | `isnumeric()` |
| -------- | ------------: | ----------: | ------------: |
| `"5"`    |          True |        True |          True |
| `"99"`   |          True |        True |          True |
| `"²"`    |         False |        True |          True |
| `"⅕"`    |         False |       False |          True |
| `"abc"`  |         False |       False |         False |
| `"12.5"` |         False |       False |         False |
| `"-12"`  |         False |       False |         False |

### `string.lower()`

**¿Qué realiza?**
Convierte a minúsculas los caracteres del string cuando corresponde.

**¿Qué retorna?**
Un nuevo string.

El string original no se modifica.

**Ejemplos:**

```python
"PYTHON".lower()
# "python"

"HeLLo WoRLd".lower()
# "hello world"

"Atención".lower()
# "atención"
```

### `string.replace(viejo, nuevo)`

**¿Qué realiza?**
Reemplaza las apariciones de un substring por otro.

**¿Qué retorna?**
Un nuevo string con los reemplazos realizados.

El string original no se modifica.

**Ejemplos:**

```python
"Python es genial".replace("genial", "excelente")
# "Python es excelente"

"aaa".replace("a", "b")
# "bbb"

"hola hola".replace("hola", "chau")
# "chau chau"
```

### `string.split(separador=None)`

**¿Qué realiza?**
Divide un string en partes.

Si se proporciona un separador, utiliza ese texto como punto de división.

Si no se proporciona un separador, utiliza los espacios en blanco como separadores.

**¿Qué retorna?**
Una lista de strings.

**Ejemplos:**

```python
"uno,dos,tres".split(",")
# ['uno', 'dos', 'tres']

"Python es genial".split()
# ['Python', 'es', 'genial']

"a-b-c-d".split("-")
# ['a', 'b', 'c', 'd']
```

Uso habitual con `input()`:

```python
linea = input("Ingresa números: ").split()
```

Si se ingresa:

```text
10 20 30
```

el resultado será:

```python
["10", "20", "30"]
```

Para convertir los elementos a enteros:

```python
numeros = [int(x) for x in linea]
```

### `string.startswith(prefijo)`

**¿Qué realiza?**
Verifica si un string comienza con un prefijo determinado.

**¿Qué retorna?**
`True` si comienza con el prefijo y `False` en caso contrario.

**Ejemplos:**

```python
"Python".startswith("Py")
# True

"Python".startswith("python")
# False

"archivo.txt".startswith("archivo")
# True

"archivo.txt".startswith("texto")
# False
```

### `string.upper()`

**¿Qué realiza?**
Convierte a mayúsculas los caracteres del string cuando corresponde.

**¿Qué retorna?**
Un nuevo string.

El string original no se modifica.

**Ejemplos:**

```python
"python".upper()
# "PYTHON"

"HeLLo WoRLd".upper()
# "HELLO WORLD"

"Atención".upper()
# "ATENCIÓN"
```

---

## Métodos para listas

### `lista.append(elemento)`

**¿Qué realiza?**
Agrega un elemento al final de la lista.

Modifica la lista original.

**¿Qué retorna?**
`None`.

**Ejemplo:**

```python
numeros = [1, 2, 3]

numeros.append(4)

print(numeros)
# [1, 2, 3, 4]
```

### `lista.count(elemento)`

**¿Qué realiza?**
Cuenta cuántas veces aparece un elemento en la lista.

**¿Qué retorna?**
Un número entero (`int`).

**Ejemplos:**

```python
numeros = [1, 2, 2, 3, 2]

numeros.count(2)
# 3

numeros.count(5)
# 0
```

### `lista.index(elemento)`

**¿Qué realiza?**
Busca la primera aparición de un elemento en la lista.

**¿Qué retorna?**
El índice de la primera aparición.

Si el elemento no existe, produce `ValueError`.

**Ejemplos:**

```python
nombres = ["Ana", "Juan", "Lucía", "Juan"]

nombres.index("Juan")
# 1

nombres.index("Lucía")
# 2
```

### `lista.pop(indice=-1)`

**¿Qué realiza?**
Elimina y retorna un elemento de la lista.

Si no se indica un índice, elimina el último elemento.

**¿Qué retorna?**
El elemento eliminado.

**Ejemplo:**

```python
numeros = [10, 20, 30]

ultimo = numeros.pop()

print(ultimo)
# 30

print(numeros)
# [10, 20]
```

También puede indicarse un índice:

```python
numeros = [10, 20, 30]

elemento = numeros.pop(1)

print(elemento)
# 20

print(numeros)
# [10, 30]
```

### `lista.remove(elemento)`

**¿Qué realiza?**
Elimina la primera aparición del elemento indicado.

**¿Qué retorna?**
`None`.

Si el elemento no existe, produce `ValueError`.

**Ejemplo:**

```python
numeros = [10, 20, 30, 20]

numeros.remove(20)

print(numeros)
# [10, 30, 20]
```

### `lista.reverse()`

**¿Qué realiza?**
Invierte el orden de los elementos de la lista.

Modifica la lista original.

**¿Qué retorna?**
`None`.

**Ejemplo:**

```python
numeros = [1, 2, 3, 4]

numeros.reverse()

print(numeros)
# [4, 3, 2, 1]
```

### `lista.sort(reverse=False)`

**¿Qué realiza?**
Ordena los elementos de la lista modificando la lista original.

**¿Qué retorna?**
`None`.

**Ejemplo:**

```python
numeros = [3, 1, 4, 2]

numeros.sort()

print(numeros)
# [1, 2, 3, 4]
```

En orden descendente:

```python
numeros.sort(reverse=True)

print(numeros)
# [4, 3, 2, 1]
```

---

## Métodos para tuplas

Las tuplas son secuencias inmutables. Por eso no poseen métodos como `append()`, `remove()` o `sort()`.

### `tupla.count(elemento)`

**¿Qué realiza?**
Cuenta cuántas veces aparece un elemento en la tupla.

**¿Qué retorna?**
Un número entero (`int`).

**Ejemplo:**

```python
datos = (1, 2, 2, 3, 2)

datos.count(2)
# 3

datos.count(5)
# 0
```

### `tupla.index(elemento)`

**¿Qué realiza?**
Busca la primera aparición de un elemento.

**¿Qué retorna?**
El índice de la primera aparición.

Si el elemento no existe, produce `ValueError`.

**Ejemplo:**

```python
datos = ("Ana", "Juan", "Lucía", "Juan")

datos.index("Juan")
# 1

datos.index("Lucía")
# 2
```

---

## Métodos para diccionarios

### `diccionario.get(clave, valor_por_defecto=None)`

**¿Qué realiza?**
Obtiene el valor asociado a una clave.

Si la clave no existe, retorna el valor por defecto. Si no se indica un valor por defecto, retorna `None`.

**¿Qué retorna?**
El valor asociado o el valor por defecto.

**Ejemplo:**

```python
datos = {
    "nombre": "Juan",
    "edad": 25
}

datos.get("nombre")
# 'Juan'

datos.get("ciudad")
# None

datos.get("ciudad", "N/A")
# 'N/A'
```

Para comprobar la existencia de una clave puede utilizarse el operador `in`:

```python
if "edad" in datos:
    print("La clave existe")
```

### `diccionario.items()`

**¿Qué realiza?**
Proporciona los pares clave-valor del diccionario.

**¿Qué retorna?**
Un objeto `dict_items`, iterable, cuyos elementos son tuplas:

```text
(clave, valor)
```

**Ejemplo:**

```python
productos = {
    "pan": 2.50,
    "leche": 3.20
}

for nombre, precio in productos.items():
    print(nombre, precio)

# Salida:
# pan 2.5
# leche 3.2
```

Puede convertirse a una lista:

```python
list(productos.items())
# [('pan', 2.5), ('leche', 3.2)]
```

### `diccionario.keys()`

**¿Qué realiza?**
Proporciona las claves del diccionario.

**¿Qué retorna?**
Un objeto `dict_keys`, iterable.

**Ejemplo:**

```python
datos = {
    "nombre": "Ana",
    "edad": 20
}

datos.keys()
# dict_keys(['nombre', 'edad'])

list(datos.keys())
# ['nombre', 'edad']
```

### `diccionario.pop(clave)`

### `diccionario.pop(clave, valor_por_defecto)`

**¿Qué realiza?**
Elimina una clave del diccionario y retorna el valor asociado.

Si la clave no existe y se proporciona un valor por defecto, retorna ese valor sin producir un error.

**¿Qué retorna?**
El valor asociado a la clave eliminada o el valor por defecto.

**Ejemplo:**

```python
datos = {
    "nombre": "Ana",
    "edad": 20
}

edad = datos.pop("edad")

print(edad)
# 20

print(datos)
# {'nombre': 'Ana'}
```

Con valor por defecto:

```python
datos.pop("ciudad", "No existe")
# 'No existe'
```

### `diccionario.values()`

**¿Qué realiza?**
Proporciona los valores almacenados en el diccionario.

**¿Qué retorna?**
Un objeto `dict_values`, iterable.

**Ejemplo:**

```python
calificaciones = {
    "María": 9.5,
    "Pedro": 8.0,
    "Ana": 9.0
}

list(calificaciones.values())
# [9.5, 8.0, 9.0]
```

Puede combinarse con otras funciones:

```python
promedio = sum(calificaciones.values()) / len(calificaciones)

print(promedio)
# 8.833333333333334
```

---

## Métodos para sets

### `conjunto.add(elemento)`

**¿Qué realiza?**
Agrega un elemento al conjunto.

Si el elemento ya pertenece al conjunto, el conjunto permanece sin cambios, porque un `set` no contiene elementos duplicados.

**¿Qué retorna?**
`None`.

**Ejemplo:**

```python
unicos = {"Ana", "Juan", "Pedro"}

unicos.add("Lucía")
```

El conjunto contiene los cuatro elementos, pero no debe suponerse un orden particular al mostrarlo.

### `conjunto.discard(elemento)`

**¿Qué realiza?**
Elimina un elemento del conjunto si está presente.

Si el elemento no existe, no produce un error.

**¿Qué retorna?**
`None`.

**Ejemplo:**

```python
numeros = {1, 2, 3}

numeros.discard(2)

print(numeros)
# {1, 3}
```

Si no existe:

```python
numeros.discard(5)
```

El conjunto permanece sin cambios.

### `conjunto.difference(otro_conjunto)`

**¿Qué realiza?**
Obtiene los elementos que pertenecen al primer conjunto pero no al segundo.

**¿Qué retorna?**
Un nuevo `set`.

Los conjuntos originales no se modifican.

**Ejemplo:**

```python
a = {1, 2, 3}
b = {2, 3, 4}

resultado = a.difference(b)

print(resultado)
# {1}
```

### `conjunto.intersection(otro_conjunto)`

**¿Qué realiza?**
Obtiene los elementos que pertenecen a ambos conjuntos.

**¿Qué retorna?**
Un nuevo `set`.

**Ejemplo:**

```python
a = {1, 2, 3}
b = {2, 3, 4}

resultado = a.intersection(b)

print(resultado)
# {2, 3}
```

### `conjunto.remove(elemento)`

**¿Qué realiza?**
Elimina un elemento del conjunto.

Si el elemento no existe, produce `KeyError`.

**¿Qué retorna?**
`None`.

**Ejemplo:**

```python
numeros = {1, 2, 3}

numeros.remove(2)

print(numeros)
# {1, 3}
```

### `conjunto.union(otro_conjunto)`

**¿Qué realiza?**
Obtiene un nuevo conjunto que contiene los elementos de ambos conjuntos, sin duplicados.

**¿Qué retorna?**
Un nuevo `set`.

Los conjuntos originales no se modifican.

**Ejemplo:**

```python
a = {1, 2, 3}
b = {3, 4, 5}

resultado = a.union(b)

print(resultado)
# {1, 2, 3, 4, 5}
```

---

## Resumen de funciones y métodos

| Categoría        | Funciones / métodos                                                                                                                               |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Generales**    | `all`, `any`, `dict`, `enumerate`, `float`, `input`, `int`, `len`, `list`, `max`, `min`, `print`, `range`, `set`, `sorted`, `sum`, `tuple`, `zip` |
| **Strings**      | `isalnum`, `isalpha`, `isdecimal`, `isdigit`, `isnumeric`, `lower`, `replace`, `split`, `startswith`, `upper`                                     |
| **Listas**       | `append`, `count`, `index`, `pop`, `remove`, `reverse`, `sort`                                                                                    |
| **Tuplas**       | `count`, `index`                                                                                                                                  |
| **Diccionarios** | `get`, `items`, `keys`, `pop`, `values`                                                                                                           |
| **Sets**         | `add`, `discard`, `difference`, `intersection`, `remove`, `union`                                                                                 |

---

## Distinciones importantes

### Funciones y métodos

Las funciones incorporadas se invocan directamente:

```python
len(lista)
sorted(lista)
sum(numeros)
```

Los métodos se invocan sobre un objeto:

```python
lista.append(10)
texto.lower()
diccionario.items()
```

### `sorted()` y `sort()`

`sorted()` es una función y retorna una nueva lista:

```python
numeros = [3, 1, 2]

ordenados = sorted(numeros)

print(numeros)
# [3, 1, 2]

print(ordenados)
# [1, 2, 3]
```

`sort()` es un método de las listas y modifica la lista original:

```python
numeros = [3, 1, 2]

resultado = numeros.sort()

print(numeros)
# [1, 2, 3]

print(resultado)
# None
```

### Métodos que modifican la colección

Algunos métodos modifican el objeto original y retornan `None`:

```python
lista.append(4)
lista.remove(4)
lista.reverse()
lista.sort()

conjunto.add(4)
conjunto.remove(4)
conjunto.discard(4)
```

Otros métodos retornan información o una nueva colección:

```python
lista.pop()
lista.count(4)
lista.index(4)

conjunto.union(otro)
conjunto.intersection(otro)
conjunto.difference(otro)
```

### `append()` y `extend()`

`append()` agrega un único elemento:

```python
lista = [1, 2]

lista.append([3, 4])

print(lista)
# [1, 2, [3, 4]]
```

`extend()` agrega los elementos de un iterable:

```python
lista = [1, 2]

lista.extend([3, 4])

print(lista)
# [1, 2, 3, 4]
```

### `remove()` y `pop()`

`remove()` recibe un elemento y lo elimina:

```python
lista = [10, 20, 30]

lista.remove(20)

print(lista)
# [10, 30]
```

`pop()` recibe un índice y elimina y retorna el elemento ubicado en esa posición:

```python
lista = [10, 20, 30]

valor = lista.pop(1)

print(valor)
# 20

print(lista)
# [10, 30]
```

### `remove()` y `discard()` en sets

En un conjunto:

```python
conjunto.remove(5)
```

produce `KeyError` si `5` no existe.

En cambio:

```python
conjunto.discard(5)
```

no produce error si `5` no existe.

### `get()` y acceso mediante `[]` en diccionarios

El acceso mediante `[]` produce `KeyError` si la clave no existe:

```python
datos = {"nombre": "Ana"}

datos["edad"]
# KeyError
```

`get()` permite proporcionar un valor por defecto:

```python
datos.get("edad", 0)
# 0
```

### `items()`, `keys()` y `values()`

En un diccionario:

```python
datos = {
    "nombre": "Ana",
    "edad": 20
}
```

se obtiene:

```python
datos.keys()
# dict_keys(['nombre', 'edad'])

datos.values()
# dict_values(['Ana', 20])

datos.items()
# dict_items([('nombre', 'Ana'), ('edad', 20)])
```

`items()` proporciona pares:

```text
(clave, valor)
```

`keys()` proporciona claves.

`values()` proporciona valores.

### Strings y caracteres

Un string es una secuencia de caracteres:

```python
texto = "Hola"
```

Puede pensarse conceptualmente como:

```text
"H" "o" "l" "a"
```

Por eso los métodos como:

```python
"99".isdigit()
# True
```

analizan los caracteres que forman el string.

En este caso:

```text
"9" "9"
```

Los dos caracteres son dígitos.

### `isdecimal()`, `isdigit()` e `isnumeric()`

Estos tres métodos trabajan sobre los caracteres del string y utilizan las categorías numéricas definidas por Unicode.

Su relación general es:

```text
isdecimal() ⊂ isdigit() ⊂ isnumeric()
```

Por ejemplo:

```python
"²".isdecimal()
# False

"²".isdigit()
# True

"²".isnumeric()
# True
```

y:

```python
"⅕".isdecimal()
# False

"⅕".isdigit()
# False

"⅕".isnumeric()
# True
```

Para validar una entrada que deba representar un entero decimal en una aplicación, `isdigit()` no siempre es suficiente, porque no acepta signos como `-` y tampoco reemplaza la conversión mediante `int()`.

---

## Nota sobre las salidas de conjuntos

Los elementos de un `set` no deben considerarse ordenados.

Por eso, aunque conceptualmente:

```python
{1, 2, 3}
```

contenga esos tres elementos, no debe utilizarse el orden mostrado por `print()` como parte del resultado esperado.

Para obtener una representación ordenada puede utilizarse:

```python
sorted({3, 1, 2})
# [1, 2, 3]
```

---

## Resumen conceptual

| Operación                   | Resultado principal            |
| --------------------------- | ------------------------------ |
| `len(objeto)`               | Cantidad de elementos          |
| `list(iterable)`            | Nueva lista                    |
| `tuple(iterable)`           | Nueva tupla                    |
| `set(iterable)`             | Nuevo conjunto, sin duplicados |
| `dict(iterable)`            | Nuevo diccionario              |
| `sorted(iterable)`          | Nueva lista ordenada           |
| `sum(iterable)`             | Suma de los elementos          |
| `min(iterable)`             | Menor elemento                 |
| `max(iterable)`             | Mayor elemento                 |
| `all(iterable)`             | `True` si todos son verdaderos |
| `any(iterable)`             | `True` si alguno es verdadero  |
| `enumerate(iterable)`       | Índice y elemento              |
| `zip(iterable1, iterable2)` | Elementos agrupados en tuplas  |

---

## Notas

* Las funciones y métodos de este documento constituyen una referencia de las operaciones utilizadas para trabajar con las colecciones y strings abordados en el capítulo.
* Las listas son mutables; las tuplas son inmutables.
* Los diccionarios almacenan asociaciones entre claves y valores.
* Los sets almacenan elementos únicos y no deben utilizarse suponiendo un orden determinado.
* Los strings son secuencias inmutables de caracteres.
* `sorted()` retorna una nueva lista; `list.sort()` modifica la lista original.
* `append()`, `remove()`, `reverse()`, `sort()`, `add()` y `discard()` modifican la colección y retornan `None`.
* `items()`, `keys()` y `values()` retornan objetos de vista de diccionario, no listas.
* `input()` siempre retorna un `str`; cuando se necesita otro tipo de dato debe realizarse la conversión correspondiente.
* `range()` retorna un objeto `range`, no una lista.
* `isdecimal()`, `isdigit()` e `isnumeric()` analizan caracteres de un string y no deben interpretarse como comprobaciones de rangos numéricos.
