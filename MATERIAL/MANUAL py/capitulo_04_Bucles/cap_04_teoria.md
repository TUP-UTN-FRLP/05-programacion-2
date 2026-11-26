# Bucles

_Repeticiones condicionales y fijas_

## ¿Por qué leemos este capítulo?

Hasta acá tomamos decisiones únicas: ejecutar un bloque u otro según una condición. Pero muchas veces necesitamos repetir una acción: pedir 10 notas, procesar una lista de nombres, calcular la suma de todos los números del 1 al 100. Para eso están los bucles.

En C teníamos `for`, `while` y `do-while`, todos apoyados en un contador manual. Python simplifica: elimina el `do-while`, mantiene `while` casi idéntico, y transforma el `for` en algo completamente distinto - más limpio, más potente, y estrechamente ligado a las estructuras que vemos a continuación: listas y tuplas.

## Listas y Tuplas: dos colecciones de datos

Antes de recorrer con un bucle, necesitamos saber qué vamos a recorrer. En Python, la colección más habitual es la lista.

### Listas (list)

Una lista es una colección ordenada y mutable (se puede modificar). Se escribe entre corchetes `[ ]`.

**Creación:**

```python
notas = [7, 8, 5, 9, 6]
nombres = ["Ana", "Juan", "Pedro"]
mezclada = [1, "hola", 3.14, True]     # Python permite mezclar tipos
vacia = []
```

**Otra forma de crear listas: la función `list()`**

Además de los corchetes, existe la función `list()` que convierte cualquier iterable en lista. Los casos más comunes:

```python
numeros = list(range(1, 6))         # [1, 2, 3, 4, 5]
letras = list("Python")             # ['P', 'y', 't', 'h', 'o', 'n']
claves = list({"a": 1, "b": 2})     # ['a', 'b']  (las claves del dict)
```

Te llamará la atención la función `range()`. Es un objeto especial que va generando los números a medida que se los pide. En un `for` funciona igual que si lo envolvés con `list()`. Es una forma rápida de asignación, un rango que introduce el primer valor, los intermedios, pero no el último.

La tercera línea lo veremos en el próximo capítulo.

![](img/cap04_img01.jpeg)

**EJERCICIO 1**

Convertí en lista los números del 5 al 20, la palabra "programación" letra por letra, y `range(0, 100, 10)`.

> Ver código en el archivo `.py`.

**Acceso por índice:** igual que en C, arrancando desde 0:

```python
notas[0]     # 7   (primer elemento)
notas[2]     # 5   (tercer elemento)
notas[-1]    # 6   (¡último elemento! esto no existe en C)
notas[-2]    # 9   (anteúltimo)
```

**Modificación:** a diferencia de C, las listas crecen o achican sin que declares un tamaño:

```python
notas.append(10)      # Agrega al final: [7, 8, 5, 9, 6, 10]
notas.insert(0, 4)    # Inserta en la posición indicada
notas[0] = 4          # Cambia el valor en esa posición
notas.remove(5)       # Elimina el primer 5 que encuentre
notas.pop()           # Elimina el último y lo devuelve
del notas[0]          # Elimina el elemento en la posición 0
len(notas)            # Cantidad de elementos
```

**Rebanadas (slicing):** otra cosa que en C requeriría un bucle:

```python
notas[1:4]    # Del índice 1 al 3 (el 4 no se incluye)
notas[:3]     # Los primeros 3
notas[2:]     # Del índice 2 hasta el final
notas[::-1]   # La lista al revés
```

![](img/cap04_img01.jpeg)

**EJERCICIO 2**

Creá una lista con las temperaturas de la última semana `[18, 22, 25, 21, 19, 17, 20]`. Mostrá la primera, la última, las primeras tres, y la lista al revés.

> Ver código en el archivo `.py`.

**Comparación de listas con `==`, `<`, `>` (comparación lexicográfica)**

Dos listas se pueden comparar directamente con `==`, `!=`, `<`, `>`:

```python
[1, 2, 3] == [1, 2, 3]     # True
[1, 2, 3] != [1, 2, 4]     # True
[1, 2, 3] < [1, 2, 4]      # True   (comparación elemento a elemento)
[1, 2] < [1, 2, 0]         # True   (la más corta es "menor" si empatan)
```

La comparación es lexicográfica, como en un diccionario: se comparan los primeros elementos, si son iguales los segundos y así. La primera diferencia decide.

> **Ojo:** No se pueden mezclar tipos. `[1, 2] < ["a", "b"]` da error porque Python no sabe comparar un entero con un string.

**Asignar sobre una rebanada, slicing (reemplazar un tramo)**

El slicing no solo sirve para leer: también se puede escribir sobre él, reemplazando un tramo entero por otros elementos, incluso de distinto tamaño:

```python
letras = ['a', 'b', 'c', 'd', 'e']
letras[1:3] = ['X', 'Y', 'Z']    # Reemplaza posiciones 1 y 2 por tres elementos
print(letras)                    # ['a', 'X', 'Y', 'Z', 'd', 'e']

letras[1:4] = []                 # Elimina el tramo (equivale a del letras[1:4])
print(letras)                    # ['a', 'd', 'e']
```

![](img/cap04_img01.jpeg)

**EJERCICIO 3**

Dada la lista `["Ana", "Juan", "Pedro", "Lucía", "Diego"]`, reemplazar los dos del medio (Pedro y Lucía) por `["Sofía", "Martín", "Camila"]`. Después, borrar los dos primeros usando asignación de slicing.

> Ver código en el archivo `.py`.

### Tuplas (tuple)

Una tupla es una colección ordenada e inmutable (una vez creada, no se modifica). Se escribe entre paréntesis `( )`:

```python
punto = (3, 5)
colores_rgb = (255, 128, 0)
vocales = ('a', 'e', 'i', 'o', 'u')     # la que ya usamos en el capítulo anterior
```

Se recorre y se accede por índice igual que las listas, pero NO se puede modificar:

```python
punto[0]         # 3
punto[0] = 10    # TypeError: 'tuple' object does not support item assignment
```

### ¿Cuándo usar cuál?

| Situación | Elegí |
| --- | --- |
| Los datos van a cambiar (agregar, quitar, ordenar) | Lista |
| Los datos son fijos (coordenadas, días de la semana, constantes) | Tupla |
| Querés proteger los datos de modificaciones accidentales | Tupla |
| Necesitás usarlos como clave de un diccionario (lo veremos en el próximo capítulo) | Tupla (una lista no puede ser clave) |

**Regla práctica:** si dudás, usá lista. La tupla es la elección deliberada cuando querés dejar claro que "esto no debe cambiar".

![](img/cap04_img01.jpeg)

**EJERCICIO 4**

Creá una tupla con las coordenadas de un punto en el plano y otra con los tres colores primarios RGB. Intentá modificar el primer valor de una de ellas y observá el error que da Python.

> Ver código en el archivo `.py`.

El error de Python es explícito: no se puede modificar. Si algún día necesitás cambiar la coordenada, tenés que crear una tupla nueva: `punto = (50, punto[1])`.

## El bucle WHILE: casi idéntico a C

Repite un bloque mientras una condición sea verdadera. La sintaxis es la misma lógica que en C, con los cambios habituales de Python (dos puntos, indentación, sin paréntesis).

En C:

```c
int i = 0;
while (i < 5) {
    printf("%d\n", i);
    i++;
}
```

En Python:

```python
i = 0
while i < 5:
    print(i)
    i += 1      # Python no tiene el operador i++
```

> **CUIDADO:** Python no tiene los operadores `++` ni `--` de C. En su lugar se usa `i += 1` que equivale a `i = i + 1` / `i -= 1` que equivale a `i = i - 1`.

No existe `do-while` en Python. En C teníamos `do { ... } while (cond);` para ejecutar al menos una vez y después chequear. El equivalente pythónico es el patrón `while True` con `break`, que vas a ver seguido:

```python
while True:
    dato = input("Ingresá un valor (o 'fin'): ")
    if dato == "fin":
        break
    print(f"Procesando: {dato}")
```

![](img/cap04_img01.jpeg)

**EJERCICIO 5**

Pedir números al usuario e ir acumulando su suma. Cortar cuando la suma pase de 100 e imprimir cuántos números hicieron falta.

> Ver código en el archivo `.py`.

Fijate el patrón: la variable que controla el `while` (`suma`) tiene que estar definida antes del bucle y modificarse adentro. Si no se modifica adentro, entrás en un bucle infinito, el error clásico del `while`.

## El bucle FOR: el gran cambio respecto de C

Esta es la diferencia más importante entre C y Python.

En C, el `for` era un `while` con contador integrado:

```c
for (int i = 0; i < 10; i++) {
    printf("%d\n", i);
}
```

En Python, el `for` no cuenta: recorre una colección, que veremos en el próximo capítulo. Podés leerlo casi como en castellano: "para cada elemento de esta lista, hacé esto".

```python
notas = [7, 8, 5, 9, 6]
for nota in notas:
    print(nota)
```

No hay índice, no hay `i++`, no hay condición de corte. Python le pide un elemento a la lista, se lo pasa a la variable `nota`, ejecuta el bloque, y cuando no quedan más elementos, termina. Es imposible pasarse del final por error.

**Alternativa**

Python también permite el estilo con índice, y a veces es necesario (típicamente cuando querés modificar los elementos mientras los recorrés).

Usamos una función `len()` para encontrar el tamaño de la lista, en el caso siguiente es 5, y si solo introducimos ese valor en el `range` este recorre 5 lugares:

```python
notas = [7, 8, 5, 9, 6]
for i in range(len(notas)):
    notas[i] = notas[i] * 2       # Multiplicamos cada nota por 2
```

Si solo querés leer los valores, quedate con el `for` "pythónico" (`for nota in notas`). El estilo con índice se guarda para cuando realmente lo necesites.

![](img/cap04_img01.jpeg)

**EJERCICIO 6**

Dada la lista `precios = [1500, 2300, 800, 4200, 1900]`, calcular el total a pagar y el precio promedio.

> Ver código en el archivo `.py`.

Este es el patrón acumulador: una variable arranca en 0 y va sumando en cada vuelta. El mismo esqueleto sirve para contar, multiplicar (arrancando en 1 en lugar de 0), o construir un string.

### range(): cuando sí necesitás contar

¿Y si querés hacer algo N veces, como el `for (i = 0; i < 10; i++)` de C? Para eso está `range()`:

```python
for i in range(5):
    print(i)
# Imprime: 0, 1, 2, 3, 4
```

`range()` genera una secuencia de números. Tiene tres formas:

```python
range(5)           # 0, 1, 2, 3, 4          # (para en 5, sin incluirlo)
range(2, 8)        # 2, 3, 4, 5, 6, 7        # (desde 2 hasta antes de 8)
range(0, 20, 2)    # 0, 2, 4, 6, 8, ... 18   # (paso de 2)
range(10, 0, -1)   # 10, 9, 8, ... 1         # (cuenta regresiva, no llega al 0)
```

Como en las rebanadas, el segundo argumento siempre es exclusivo: NUNCA SE INCLUYE.

![](img/cap04_img01.jpeg)

**EJERCICIO 7**

Imprimir todos los números pares del 2 al 20 usando `range()` con paso. Después, la cuenta regresiva de 10 a 1 en la misma línea.

> Ver código en el archivo `.py`.

El `end=" "` en el segundo `print()` reemplaza el salto de línea por un espacio, para que salgan todos los números en la misma línea.

### enumerate(): ¿y si necesito el índice Y el valor?

A veces sí querés saber en qué posición vas mientras recorrés. Podrías hacerlo con `range(len(lista))`, pero Python tiene algo más limpio:

```python
notas = [7, 8, 5, 9, 6]
for indice, nota in enumerate(notas):
    print(f"La nota número {indice + 1} es {nota}")
```

![](img/cap04_img01.jpeg)

**EJERCICIO 8**

Dada una lista de tareas pendientes, imprimir un checklist numerado empezando en 1.

> Ver código en el archivo `.py`.

Fijate el parámetro `start=1`: por defecto `enumerate()` arranca en 0, pero al mostrarle esto a un humano casi siempre queremos empezar en 1.

### zip(): recorrer dos listas en paralelo

```python
nombres = ["Ana", "Juan", "Pedro"]
notas = [8, 6, 9]
for nombre, nota in zip(nombres, notas):
    print(f"{nombre} sacó {nota}")
```

![](img/cap04_img01.jpeg)

**EJERCICIO 9**

Tenés dos listas paralelas, una con productos y otra con precios. Imprimir el catálogo y calcular el total.

> Ver código en el archivo `.py`.

`zip()` es la respuesta correcta cuando tenés datos "en paralelo" en dos listas. En el próximo capítulo vamos a ver una forma aún mejor de guardar esta información: los diccionarios.

### break y continue: interrumpir el bucle

Igual que en C:

- `break` corta el bucle por completo.
- `continue` saltea la iteración actual y pasa a la siguiente.

```python
# break: buscar un elemento y detenerse
for numero in [3, 7, 12, 5, 8]:
    if numero > 10:
        print(f"Encontré uno mayor a 10: {numero}")
        break

# continue: procesar solo los pares
for numero in range(10):
    if numero % 2 != 0:
        continue
    print(numero)     # Imprime solo 0, 2, 4, 6, 8
```

![](img/cap04_img01.jpeg)

**EJERCICIO 10**

Dada una lista de números, imprimir solo los positivos, y detenerse si encuentra un `-99` (código de "fin de datos").

> Ver código en el archivo `.py`.

Los dos usos combinados: `continue` para "este no me interesa, sigo con el próximo" y `break` para "no procesar más nada". El orden importa: primero chequeamos la condición de corte, después la de salteo.

## Funciones muy útiles para trabajar con colecciones

![](img/cap04_img02.jpeg)

Estas funciones no son "de bucles", pero aparecen todo el tiempo cuando trabajás con listas y muchas veces te evitan escribir uno:

| Función | Qué hace | Ejemplo |
| --- | --- | --- |
| `len(lista)` | Cantidad de elementos | `len([1,2,3])` ➡ 3 |
| `sum(lista)` | Suma de todos los elementos | `sum([1,2,3])` ➡ 6 |
| `max(lista)` | Mayor elemento | `max([3,1,7,2])` ➡ 7 |
| `min(lista)` | Menor elemento | `min([3,1,7,2])` ➡ 1 |
| `sorted(lista)` | Devuelve una lista nueva ordenada (no toca la original) | `sorted([3,1,2])` ➡ [1,2,3] |
| `lista.sort()` | Ordena la lista en el lugar (modifica el original) | `notas.sort()` |
| `reversed(lista)` | Recorre al revés | `for x in reversed(lista):` |
| `any(lista)` | True si al menos un elemento es True | `any([False, True, False])` ➡ True |
| `all(lista)` | True si todos son True | VER capítulo anterior |

> **TIP importante:** `sorted()` te devuelve una lista nueva, `.sort()` modifica la original y no devuelve nada (¡ojo, es un error clásico escribir `notas = notas.sort()` y quedarse con `None`!).

![](img/cap04_img01.jpeg)

**EJERCICIO 11**

Dada la lista de notas `[7, 4, 9, 6, 8, 3, 10, 5]`, mostrar la cantidad, el promedio, la nota más alta y la más baja. Después, ordenarla de mayor a menor sin modificar la original.

> Ver código en el archivo `.py`.

Usamos `sorted()` (que devuelve una lista nueva) en vez de `.sort()` (que modifica la original) porque el enunciado pedía no tocar la lista original. Si hubiéramos hecho `notas.sort()`, la línea siguiente imprimiría la lista ordenada, no la original.

## TIP: el else de los bucles (raro y útil)

Python tiene una peculiaridad que no existe en C: los bucles pueden tener un `else` que se ejecuta solo si el bucle terminó sin usar `break`. Es raro y muchos programadores no lo conocen, pero es limpísimo para búsquedas:

```python
buscado = 12
for numero in [3, 7, 12, 5, 8]:
    if numero == buscado:
        print("Encontrado en la lista")
        break
else:
    print(f"{buscado} no está en la lista")
```

Ojo: el `else` es del `for`, no del `if`. Se ejecuta solo cuando el bucle termina de recorrer todo sin haber ejecutado un `break`. Es la manera más limpia de escribir "buscar y avisar si no está".

![](img/cap04_img01.jpeg)

**EJERCICIO 12**

Buscar si un número dado está en una lista y avisar si lo encontraste o no, usando `for...else`.

> Ver código en el archivo `.py`.
