# Comprehensions

> Del bucle a la expresión.

## ¿Por qué leemos este capítulo?

En el capítulo de funciones vimos que muchas de las que escribíamos hacían lo mismo por debajo: recorrer una colección con for, filtrar con if, y armar una lista, diccionario o set nuevo con el resultado. Ese patrón es tan frecuente que Python le dio una sintaxis propia, más compacta y legible: las comprensiones.

Una comprensión es una expresión que construye una colección a partir de otra, en una sola línea. Es un **idiom pythónico central**: aparece en librerías, tutoriales, respuestas de Stack Overflow y código profesional. **No dominarla es leer Python "a medias"**.

Hay cuatro tipos de comprensiones…

- …de lista
- …de diccionario
- …de set
- …generadoras.

Las tres primeras son variaciones de la misma idea con distintos paréntesis, la cuarta introduce un concepto nuevo (**lazy evaluation**) que vale la pena ver, aunque sea al pasar.

Este capítulo **es corto en teoría, pero rico en práctica**. La comprensión no es difícil de entender, es difícil de acostumbrarse a leer. Los mini-ejercicios y los 20 integradores están pensados para que la sintaxis se vuelva automática.

## Comprensiones de lista

### El patrón que reemplaza

Empezamos comparando. Este bucle, que ya escribimos decenas de veces:

```python
cuadrados = []
for x in range(10):
    cuadrados.append(x ** 2)
```

Se puede escribir en una sola línea con una **comprensión de lista**:

```python
cuadrados = [x ** 2 for x in range(10)]
```

Los dos producen [0, 1, 4, 9, 16, 25, 36, 49, 64, 81]. La versión con comprensión se lee de izquierda a derecha como si fuera lenguaje natural:

*"una lista con* ***x ** 2*** *para cada* ***x*** *en* ***range(10)****"*

### Anatomía de una comprensión

Toda comprensión de lista tiene esta estructura entre corchetes:

```text
[ EXPRESIÓN for VARIABLE in ITERABLE ]
```

- **EXPRESIÓN:** qué guardar en cada vuelta (puede usar la variable).
- **VARIABLE:** cómo se va a llamar cada elemento en cada iteración.
- **ITERABLE:** de dónde sacar los elementos (una lista, un rango, un string, un diccionario…).

En cuadrados = [x ** 2 for x in range(10)]:

- EXPRESIÓN: x ** 2
- VARIABLE: x
- ITERABLE: range(10)

#### EJERCICIO 1

Escribí una comprensión que genere una lista con los números del 1 al 10 multiplicados por 3.

*Ver código en el archivo `.py` correspondiente.*

### Con filtro (agregar un if)

Se puede agregar un if al final para quedarnos solo con algunos elementos:

```python
pares = [x for x in range(20) if x % 2 == 0]
# [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
```

Se lee:

*"una lista con x para cada x en range(20) siempre que x sea par".*

La estructura completa queda así:

```text
[ EXPRESIÓN for VARIABLE in ITERABLE if CONDICIÓN ]
```

Otro ejemplo, más real:

```python
nombres = ["Ana", "Sofía", "Juan", "Federico", "Ío"]
largos = [n for n in nombres if len(n) > 4]
# ['Sofía', 'Federico']
```

#### EJERCICIO 2

Dada la lista [15, 22, 8, 34, 7, 41, 19, 60], obtener una lista solo con los números mayores a 20.

*Ver código en el archivo `.py` correspondiente.*

### Con transformación Y filtro

Los dos combinados: transformamos con la expresión, filtramos con el if.

```python
# Cuadrados de los pares del 0 al 9
[x ** 2 for x in range(10) if x % 2 == 0]
# [0, 4, 16, 36, 64]
```

Se lee:

*"una lista con x ** 2 para cada x en range(10) siempre que x sea par".*

**El orden importa:** en la sintaxis, primero va el for y después el if. Pero en la lectura, hay que pensarlo al revés: **Python primero filtra con el if, y a lo que queda le aplica la expresión.**

#### EJERCICIO 3

Dada una lista de precios [500, 1200, 800, 1500, 950, 2000, 3500], generar una lista con los precios en pesos-con-IVA (21%) pero solo de los productos que originalmente costaban más de $1000.

*Ver código en el archivo `.py` correspondiente.*

### Recorriendo un string

Los strings también se recorren, y también sirven para comprensiones:

```python
frase = "Hola Mundo"
vocales_en_frase = [letra for letra in frase.lower() if letra in "aeiou"]
print(vocales_en_frase)     # ['o', 'a', 'u', 'o']
```

#### EJERCICIO 4

Dada una frase ingresada por el usuario, generá una lista con solo las letras (sin espacios ni signos).

*Ver código en el archivo `.py` correspondiente.*

### Recorriendo colecciones más complejas

La comprensión también se lleva bien con enumerate(), zip(), .items():

```python
# Pares (índice, nombre) solo para los índices pares
nombres = ["Ana", "Juan", "Pedro", "Lucía", "Diego"]
pares_indice = [(i, n) for i, n in enumerate(nombres) if i % 2 == 0]
# [(0, 'Ana'), (2, 'Pedro'), (4, 'Diego')]

# Combinar dos listas paralelas con zip
productos = ["pan", "leche", "queso"]
precios = [500, 800, 1200]
etiquetas = [f"{p}: ${pr}" for p, pr in zip(productos, precios)]
# ['pan: $500', 'leche: $800', 'queso: $1200']
```

Todo lo que aprendiste en el capítulo de bucles se aplica aquí, la comprensión es solo una forma más compacta de escribir el mismo for.

## Comprensiones de diccionario

La misma idea, pero para construir un diccionario. Se usan llaves {} y clave: valor como expresión:

```text
{ CLAVE : VALOR for VARIABLE in ITERABLE [ if CONDICIÓN ] }
```

```python
# Número ➡ cuadrado
{x: x ** 2 for x in range(5)}
# {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# Precios con IVA aplicado
precios = {"pan": 500, "leche": 800, "yerba": 3000}
con_iva = {producto: precio * 1.21 for producto, precio in precios.items()}
# {'pan': 605.0, 'leche': 968.0, 'yerba': 3630.0}

# Filtrar y transformar a la vez: solo productos caros, con descuento
descuentos = {p: v * 0.8 for p, v in precios.items() if v > 700}
# {'leche': 640.0, 'yerba': 2400.0}
```

Fijate la simetría con el capítulo de colecciones: cuando queríamos invertir un diccionario ({"a": 1, "b": 2} ➡ {1: "a", 2: "b"}), lo hacíamos con un bucle. En comprensión:

```python
original = {"a": 1, "b": 2, "c": 3}
invertido = {v: k for k, v in original.items()}
# {1: 'a', 2: 'b', 3: 'c'}
```

Una línea. El patrón invertir-un-diccionario se vuelve idiomático.

### EJERCICIO 5

Dada la lista ["Ana", "Juan", "Pedro", "Lucía"], generá un diccionario donde la clave sea el nombre y el valor su longitud.

*Ver código en el archivo `.py` correspondiente.*

## Comprensiones de set

Igual que las de lista, pero con llaves {} y sin dos puntos. El resultado no tiene orden ni repetidos:

```python
# Vocales presentes en una frase (sin repetir)
{letra for letra in "hola mundo python" if letra in "aeiou"}
# {'a', 'o', 'u'}

# Longitudes únicas de una lista de palabras
palabras = ["sol", "luna", "sol", "estrella", "sol", "cielo"]
longitudes_unicas = {len(p) for p in palabras}
# {3, 4, 5, 8}
```

**Ojo:**

{} sin dos puntos es un set, con dos puntos es un diccionario. Un set vacío se hace con set(), no con {}, eso ya lo vimos en Colecciones.

Para las comprensiones vale la misma regla, **si hay :** es dict, **si no hay:** es set.

### EJERCICIO 6

Dada la frase "el perro y el gato y el perro", obtener el set de palabras únicas.

*Ver código en el archivo `.py` correspondiente.*

Notá que esto es equivalente a set(frase.split()), dos maneras válidas de conseguir lo mismo. La comprensión gana cuando hay una transformación o filtro para el caso puro "eliminar duplicados", la conversión directa a set() es más simple.

## Comprensiones generadoras: un vistazo

Una comprensión generadora usa paréntesis () en lugar de corchetes o llaves:

```python
suma_cuadrados = sum(x ** 2 for x in range(10))
print(suma_cuadrados)     # 285
```

Se parece a una comprensión de lista, **pero no arma la lista en memoria**. Genera los valores uno por uno, **a demanda**. La diferencia solo se nota con colecciones grandes:

```python
# Comprensión de lista: crea la lista
# de 10 millones de elementos en
# memoria
[x ** 2 for x in range(10_000_000)]

# ~400 MB de RAM
# Comprensión generadora: genera cada
# valor cuando se lo pide

(x ** 2 for x in range(10_000_000))

# unos pocos bytes
```

En la práctica se usan casi siempre encajadas dentro de otra función, sum(), max(), min(), any(), all(), que consume los valores uno por uno sin necesitar la lista entera:

```python
# ¿Hay algún número mayor a 100 en esta lista? (sin armar una lista intermedia)
hay_grandes = any(n > 100 for n in mi_lista_enorme)

# Suma de los pares del 1 al millón, sin crear la lista de pares
suma = sum(n for n in range(1_000_000) if n % 2 == 0)
```

Cuando ves una comprensión "de lista" dentro de un sum(), any(), all() o similar, muchas veces se pueden sacar los corchetes y ganar eficiencia sin cambiar nada más:

```python
sum([x ** 2 for x in range(1000)])
# OK, pero crea lista intermedia

sum(x ** 2 for x in range(1000))
# mejor: los paréntesis del sum()
# sirven de contenedor
```

Este es el único caso donde vale la pena preocuparse por generadores en Programación II. Los vas a ver más a fondo cuando llegues a Python avanzado.

## ¿Cuándo usar comprensión y cuándo no?

Las comprensiones son idiomáticas, pero no siempre son la mejor opción. Regla práctica:

- Usá comprensión cuando:
- El patrón es recorrer + (filtrar) + transformar + construir una colección.
- La expresión y el filtro son simples (una línea legible cada uno).
- No hay side effects (imprimir, escribir archivos, modificar variables externas).

```python
# Perfecto candidato
nombres_mayus = [n.upper() for n in nombres]
```

**❎** Usá for tradicional cuando:

- Hay lógica compleja: varios if/else, cálculos intermedios, acumuladores paralelos.
- Necesitás efectos secundarios (imprimir cada elemento mientras procesás, escribir a un archivo).
- El objetivo no es construir una colección (por ejemplo, solo contar o mostrar).
- La comprensión se vuelve más larga que 80 caracteres o requiere entender varias operaciones anidadas.

```python
# Ilegible aunque técnicamente funciona
[x ** 2 if x > 0 else -x ** 2 for x in nums if x != 0 and x < 100]

# Preferible con for
resultado = []
for x in nums:
    if x == 0 or x >= 100:
        continue
    if x > 0:
        resultado.append(x ** 2)
    else:
        resultado.append(-x ** 2)
```

**Regla mental:**

Si al mes vas a volver a leer tu código y vas a tener que pensarlo dos veces, no era el momento de usar comprensión.

## La trampa de las comprensiones anidadas

Se pueden anidar comprensiones para recorrer estructuras de doble nivel (una matriz, por ejemplo):

```python
matriz = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
aplanada = [x for fila in matriz for x in fila]
# [1, 2, 3, 4, 5, 6, 7, 8, 9]
```

Funciona, pero la sintaxis es engañosa: el orden de los for es de afuera hacia adentro, no como sería intuitivo.

**Regla práctica:**

Con una comprensión anidada empezamos a sospechar que un bucle sería más claro.
