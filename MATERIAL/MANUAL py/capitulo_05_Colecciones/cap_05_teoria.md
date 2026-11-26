# Colecciones

> Agrupando cosas

## ¿Por qué leemos este capítulo?

En el capítulo de bucles ya usamos listas y tuplas con soltura: creación, indexación, slicing, recorrido con for. En este capítulo profundizamos lo que quedó pendiente de esas dos y sumamos las otras dos colecciones básicas: sets (conjuntos) y diccionarios (dicts).

La razón para verlas juntas es que las cuatro son parte de la misma familia: distintas formas de agrupar datos. Cada una responde a una pregunta distinta:

- Lista: ¿cómo guardo varios datos en orden, con posibilidad de agregar y quitar?
- Tupla: ¿cómo guardo un grupo de datos que nunca va a cambiar?
- Set: ¿cómo trabajo con datos únicos, sin importarme el orden?
- Diccionario: ¿cómo asocio cada dato con una etiqueta que lo identifique?

Elegir bien entre las cuatro es una de las habilidades más importantes de un programador Python. Y cuando lleguemos a POO, los atributos de un objeto son internamente un diccionario: los alumnos que ya piensan naturalmente en términos de "clave ➡ valor" absorben POO mucho más rápido.

Como venís del capítulo anterior, ya practicaste con listas y tuplas. Los mini-ejercicios en este capítulo se concentran en lo nuevo: los métodos de lista que no vimos, las sutilezas de tupla, y las dos estructuras nuevas.

### Panorama comparativo

Antes de meternos con cada una, esta tabla es el mapa que vale la pena tener a mano todo el capítulo:

| Característica | Lista | Tupla | Set | Diccionario |
| --- | --- | --- | --- | --- |
| Sintaxis | [1, 2, 3] | (1, 2, 3) | {1, 2, 3} | {"a": 1, "b": 2} |
| Mutable | Sí | No | Sí | Sí |
| Ordenada | Sí (por posición) | Sí (por posición) | No | Sí (por inserción) |
| Permite repetidos | Sí | Sí | No | No (claves únicas) |
| Acceso | Por índice l[0] | Por índice t[0] | Solo con in | Por clave d["x"] |
| Vacío | [] | () | set() | {} |

Volvé a esta tabla cada vez que dudes qué estructura elegir.

**La regla práctica:**

si dudás entre lista y otra, quedate con lista. Las otras tres son elecciones deliberadas para casos específicos.

## Listas: lo que faltaba

Ya conocés lo básico: creación con [], list(), indexación positiva y negativa, slicing, append, remove, pop, len, y recorrido con for. Nos falta ver algunas cosas que valen la pena y repasar otras importantes.

### Comparar listas

Dos listas se pueden comparar directamente con ==, !=, <, >:

```python
[1, 2, 3] == [1, 2, 3]     # True
[1, 2, 3] != [1, 2, 4]     # True
[1, 2, 3] < [1, 2, 4]      # True (comparación elemento a elemento)
[1, 2] < [1, 2, 0]         # True (la más corta es "menor" si empatan)
```

La comparación es **lexicográfica**, como en un diccionario de idioma: se comparan los primeros elementos. Si son iguales, los segundos y así. La primera diferencia decide.

### Asignar sobre una rebanada

El slicing no solo sirve para leer: también se puede escribir sobre él, reemplazando un tramo entero por otros elementos, incluso de distinto tamaño:

```python
letras = ['a', 'b', 'c', 'd', 'e']
letras[1:3] = ['X', 'Y', 'Z']       # Reemplaza posiciones 1 y 2 por tres elementos
print(letras)                        # ['a', 'X', 'Y', 'Z', 'd', 'e']

letras[1:4] = []                     # Elimina el tramo (equivale a del letras[1:4])
print(letras)                        # ['a', 'd', 'e']
```

Es la forma más limpia de hacer "reemplazar este tramo por este otro" sin tener que borrar y después insertar.

### Métodos que todavía no habíamos visto

En el capítulo anterior usamos append, remove, pop y len. La lista completa útil es:

| Método | Qué hace | Ejemplo |
| --- | --- | --- |
| insert(i, x) | Inserta x en la posición i | lst.insert(0, "primero") |
| pop(i) | Elimina y devuelve el que está en posición i | lst.pop(0) |
| clear() | Vacía la lista | lst.clear() |
| index(x) | Devuelve la posición de la primera x | lst.index("Ana") |
| count(x) | Cuántas veces aparece x | lst.count(5) |
| copy() | Devuelve una copia independiente | nueva = lst.copy() |
| extend(otra) | Agrega todos los elementos de otra lista | lst.extend([4, 5]) |

### Cuidado con las copias

Cuando escribís foo = lista, no estás copiando la lista, estás creando otra etiqueta que apunta al mismo objeto. Si modificás foo, también cambia lista:

```python
a = [1, 2, 3]
b = a              # b apunta a la misma lista que a
b.append(4)
print(a)           # [1, 2, 3, 4] cambió sin que a lo tocáramos

c = a.copy()       # c es una copia independiente
c.append(99)
print(a)           # [1, 2, 3, 4] esta vez a no cambió
```

Este es el mismo modelo de "etiquetas apuntando a objetos" que vimos en el capítulo de datos: al asignar, no copiás, compartís la referencia. Para copiar realmente, usá .copy() o list(lista).

Cuando lleguemos a funciones, esto va a ser importante: si le pasás una lista a una función y la modificás adentro, se modifica también afuera. A veces es lo que querés, a veces te sorprende.

## Tuplas: lo que faltaba

Ya usaste tuplas para agrupar valores fijos y en zip(). Repasemos dos detalles que no habíamos tocado.

### La tupla de un solo elemento

Para crear una tupla de un solo elemento hace falta una **coma final**. Sin la coma, Python interpreta que los paréntesis son de agrupación matemática:

```python
no_es_tupla = (5)        # esto es simplemente el número 5 entre paréntesis
si_es_tupla = (5,)       # esto sí es una tupla de un elemento

type(no_es_tupla)         # <class 'int'>
type(si_es_tupla)         # <class 'tuple'>
```

Es un detalle raro pero real. Se olvida hasta que rompe un programa.

### Desempaquetado de tuplas

Podés asignar los elementos de una tupla a variables distintas en una sola línea:

```python
punto = (3, 5)
x, y = punto         # x = 3, y = 5

print(x)    # 3
print(y)    # 5
```

A esto se lo llama **desempaquetado**: en lugar de acceder con punto[0] y punto[1], "abrimos" la tupla y guardamos cada elemento en su propia variable. El lado izquierdo (x, y) debe tener tantas variables como elementos la tupla, si no Python protesta.

**Esto es lo que hace el for con** zip() cuando en el capítulo anterior escribiste:

```python
nombres = ["Ana", "Juan", "Pedro"]
notas = [8, 6, 9]
for nombre, nota in zip(nombres, notas):
    print(f"{nombre}: {nota}")
```

Lo que pasa por debajo es que zip() no entrega dos valores sueltos: entrega **una tupla** en cada vuelta. Si imprimís lo que devuelve zip(), lo ves claramente:

```python
for par in zip(nombres, notas):
    print(par)

# ('Ana', 8)
# ('Juan', 6)
# ('Pedro', 9)
```

En cada iteración, par es una tupla. Cuando en cambio escribís for nombre, nota in ..., le estás diciendo a Python: "desempaquetá esa tupla en dos variables". Es el mismo mecanismo que x, y = punto, aplicado en cada vuelta del bucle. Ya lo venías usando sin saber cómo se llamaba.

### Intercambiar valores sin variable auxiliar

Y una consecuencia elegante del desempaquetado: **intercambiar los valores de dos variables en una línea**, sin necesitar una variable temporal.

```python
a = 5
b = 10

a, b = b, a          # ahora a = 10, b = 5

print(a)    # 10
print(b)    # 5
```

¿Cómo funciona? Python evalúa **primero** el lado derecho (b, a), armando la tupla (10, 5). **Después** desempaqueta esa tupla en el lado izquierdo, asignando a = 10 y b = 5.

En C esto necesitaba tres líneas y una variable auxiliar:

```python
int temp = a;
a = b;
b = temp;
```

En Python, una sola línea gracias a las tuplas.

#### EJERCICIO 1

**(en VSC abre crea una carpeta de ejercicio y crea un archivo con el nombre que quieras, escribis el codigo y guardalo como .py):**

Una función podría querer devolver dos cosas por ejemplo, dividir dos números y devolver cociente y resto. Como todavía no vimos funciones, simulá esto: guardá (cociente, resto) de dividir 47 por 5 en una tupla, y después desempaquetala en dos variables. Imprimí las dos por separado.

*Ver código en el archivo `.py` correspondiente.*

Este patrón de devolver una tupla y desempaquetarla, es muy común cuando lleguemos a funciones. Es la forma pythónica de devolver varios valores desde una función.

### ¿Cuándo elegir una tupla?

- Los datos son fijos por naturaleza: **coordenadas** (x, y), **RGB** (255, 128, 0), **fecha** (2026, 7, 24).
- Querés protegerlos de modificaciones accidentales.
- Necesitás usarlos como **clave de un diccionario** (una lista no puede ser clave, una tupla sí - lo vemos más abajo).
- Vas a devolver múltiples valores desde una función.

## Sets (conjuntos)

Un set es una colección **sin orden** y **sin repetidos**. Se escribe entre llaves { }, sin dos puntos:

```python
lenguajes = {"Python", "C", "Java", "Python"}
print(lenguajes)     # {'Python', 'C', 'Java'} - el "Python" repetido se descartó
```

### Set vacío

{} es un diccionario vacío, no un set vacío. Para crear uno vacío se usa set():

```python
vacio_dict = {}      # dict
vacio_set = set()    # set
```

### Para qué sirven

- **Eliminar duplicados de una lista** en una línea:

```python
notas = [7, 8, 5, 8, 9, 7, 10]
notas_unicas = set(notas)     # {5, 7, 8, 9, 10}
```

- **Chequear pertenencia rápido:** el operador in sobre un set es muchísimo más rápido que sobre una lista larga. Si vas a hacer muchas búsquedas, convertí a set primero.
- **Operaciones de conjuntos** (matemáticamente): unión, intersección, diferencia, diferencia simétrica:

```python
python_a = {"Ana", "Juan", "Pedro"}
python_b = {"Juan", "Lucía", "Pedro"}

python_a | python_b     # Unión: {"Ana", "Juan", "Pedro", "Lucía"}
python_a & python_b     # Intersección: {"Juan", "Pedro"}
python_a - python_b     # Diferencia: {"Ana"} (los de A que no están en B)
python_a ^ python_b     # Diferencia simétrica: {"Ana", "Lucía"}
                        # (los que están en uno u otro pero no en ambos)
```

En listas, cada una de estas líneas sería un for con in / not in, cinco veces más código.

#### EJERCICIO 2

Dos listas de amigos:

mios = ["Ana", "Juan", "Pedro", "Lucía"]

de_mi_hermano = ["Pedro", "Sofía", "Juan", "Diego"].

Averiguá quiénes son amigos de los dos, quiénes son solo míos, y quiénes son de alguno de los dos.

*Ver código en el archivo `.py` correspondiente.*

Cada relación se resuelve con un operador matemático. Elegante y directo.

### Modificación

```python
lenguajes.add("Rust")        # Agrega un elemento
lenguajes.remove("C")        # Elimina (error si no está)
lenguajes.discard("Go")      # Elimina (silencioso si no está)
lenguajes.pop()              # Elimina uno cualquiera (sin orden)
lenguajes.clear()            # Vacía el set
```

#### EJERCICIO 3

Simulá un sistema de "materias aprobadas". Empezá con un set vacío, agregá tres materias que aprobaste, y chequeá si aprobaste "Programación 2".

*Ver código en el archivo `.py` correspondiente.*

El set gana sobre la lista en tres cosas:

- no te importa el orden
- no admite repetidas
- las búsquedas con in son instantáneas.

## Diccionarios (dict)

Un diccionario es una colección de **pares clave-valor**. Es la estructura que más vas a usar en Python después de las listas, y es un puente directo hacia POO (un objeto es, conceptualmente, un diccionario con nombre y comportamiento).

```python
alumno = {
    "nombre": "Juan",
    "edad": 25,
    "carrera": "Ingeniería",
    "promedio": 8.5
}
```

Fijate lo que ganamos frente a una lista ["Juan", 25, "Ingeniería", 8.5], cada valor tiene una **etiqueta con significado**. No hay ambigüedad sobre qué es cada cosa.

### Acceso, modificación y agregado

```python
alumno["nombre"]         # "Juan"
alumno["edad"]           # 25

alumno["edad"] = 26                       # Modifica un valor existente
alumno["email"] = "juan@correo.com"       # Agrega una clave nueva
```

**Cuidado:** si accedés a una clave que no existe, obtenés un error:

```python
alumno["telefono"]       # KeyError: 'telefono'
```

Para consultar sin riesgo de error, usá el método .get():

```python
alumno.get("telefono")              # None (no existe, pero no rompe)
alumno.get("telefono", "sin dato")  # "sin dato" (valor por defecto)
```

#### EJERCICIO 4

creá un diccionario con datos de un producto (nombre, precio, stock). Después, subile el precio un 10%, agregale una clave "categoría" y consultá si tiene "descuento" (sin que rompa si no está).

*Ver código en el archivo `.py` correspondiente.*

.get(clave, valor_por_defecto) es lo que hubieras querido tener siempre en C cuando accedías a estructuras sin saber si estaban inicializadas.

### Recorrer un diccionario

Un for sobre un diccionario recorre **las claves** por defecto:

```python
for clave in alumno:
    print(clave, "->", alumno[clave])
```

Pero es más limpio pedir claves y valores juntos con .items():

```python
for clave, valor in alumno.items():
    print(f"{clave}: {valor}")
```

Acá aparece de nuevo el **desempaquetado de tuplas** que vimos hace un rato: .items() en cada vuelta entrega una tupla (clave, valor), y Python la desempaqueta automáticamente en las dos variables.

También podés recorrer solo las claves o solo los valores:

```python
for valor in alumno.values():
    print(valor)
for clave in alumno.keys():     # equivalente a for clave in alumno
    print(clave)
```

### Chequear si una clave existe, eliminar

```python
if "email" in alumno:
    print("Tiene email registrado")
del alumno["email"]              # Elimina la clave
alumno.pop("email")              # Igual, pero además devuelve el valor eliminado
alumno.pop("noexiste", None)     # Con default, no rompe si no existe
```

El operador in sobre un diccionario chequea **claves**, no valores. Es rápido, igual que en un set.

#### EJERCICIO 5

Dado un diccionario de stock, pedirle al usuario un producto y su cantidad, y "vender" (restar del stock). Si al terminar la venta el stock llega a 0, eliminar el producto del diccionario.

*Ver código en el archivo `.py` correspondiente.*

Combinamos las tres herramientas de la sección: in para chequear, acceso [clave] para modificar, del para eliminar.

### Reglas para las claves

Las claves de un diccionario tienen que ser **inmutables**: strings, números, tuplas, booleanos. Los valores pueden ser cualquier cosa, incluso otras listas o diccionarios:

```python
# Válido
tarifas = {"tarjeta": 0.05, "efectivo": 0}
coordenadas = {(0, 0): "origen", (1, 0): "derecha"}

# Inválido: la clave es una lista (mutable)
mal = {[1, 2]: "no funciona"}     # TypeError: unhashable type
```

Este es uno de los casos donde las **tuplas** son la elección obligada, no una preferencia estética: para usar una coordenada (x, y) como clave, tiene que ser una tupla, no una lista.

### Diccionarios anidados

Los valores pueden ser diccionarios, y esto es súper común:

```python
alumnos = {
    "juan_perez": {
        "nombre": "Juan Pérez",
        "edad": 25,
        "notas": [8, 7, 9]
    },
    "ana_lopez": {
        "nombre": "Ana López",
        "edad": 22,
        "notas": [10, 9, 10]
    }
}

alumnos["juan_perez"]["nombre"]      # "Juan Pérez"
alumnos["ana_lopez"]["notas"][0]     # 10
```

Ya casi parece una base de datos.

**RECORDÁ:**

Cuando lleguemos a librerías, vamos a ver que JSON, el formato estándar para intercambiar datos por internet, es exactamente esto: **diccionarios anidados**.

#### EJERCICIO 6

Con el diccionario alumnos de arriba, calcular e imprimir el promedio de notas de cada alumno.

*Ver código en el archivo `.py` correspondiente.*

Dos niveles de indirección: datos ya es el sub-diccionario del alumno, y ahí adentro accedemos a datos["notas"] como un diccionario normal. En el print usamos datos['nombre'] con comillas simples porque el f-string ya usa dobles.

### Métodos útiles

| Método | Qué hace |
| --- | --- |
| len(dic) | Cantidad de pares |
| dic.keys() | Vista de las claves |
| dic.values() | Vista de los valores |
| dic.items() | Vista de los pares (clave, valor) |
| dic.get(k, d) | Valor de k, o d si no existe |
| dic.pop(k) | Elimina y devuelve el valor de k |
| dic.update(otro) | Agrega/actualiza con los pares de otro |
| dic.clear() | Vacía el diccionario |
| dic.copy() | Copia superficial |

## Conversiones entre colecciones

Una de las cosas más útiles de trabajar con las cuatro estructuras es que **se convierten unas en otras** con una llamada al constructor.

Ya usamos list() en el capítulo anterior, el resto sigue el mismo patrón:

```python
lst = [1, 2, 2, 3, 3, 3]
tuple(lst)         # (1, 2, 2, 3, 3, 3)
set(lst)           # {1, 2, 3} elimina duplicados
list(set(lst))     # [1, 2, 3] elimina duplicados y vuelve a lista
```

De diccionario:

```python
d = {"a": 1, "b": 2, "c": 3}
list(d)            # ['a', 'b', 'c'] solo las claves
list(d.values())   # [1, 2, 3]
list(d.items())    # [('a', 1), ('b', 2), ('c', 3)] lista de tuplas
```

Y en el otro sentido, se puede construir un diccionario desde una lista de tuplas:

```python
pares = [("a", 1), ("b", 2), ("c", 3)]
dict(pares)        # {'a': 1, 'b': 2, 'c': 3}
```

Estos **idioms** aparecen todo el tiempo. Vale la pena tenerlos a mano.

### EJERCICIO 7

dada la lista ["Ana", "Juan", "Ana", "Pedro", "Juan", "Ana"], obtener una lista con los nombres únicos, ordenados alfabéticamente.

*Ver código en el archivo `.py` correspondiente.*

Encadenamos dos conversiones: primero set() para eliminar duplicados, después sorted() para ordenar (que además devuelve una lista, no un set). En una línea.

### idiom

Un **idiom** en Python es una **forma característica y estándar de resolver una tarea común**, que la comunidad Python considera "la manera correcta" de hacerlo. No es una regla del lenguaje, es una convención cultural.

La palabra viene del inglés "idiom", como los modismos en un idioma humano ("costar un ojo de la cara" no se traduce literalmente, es una expresión hecha). En Python pasa lo mismo: hay formas idiomáticas que un programador Python reconoce al instante.

### pythónico

describe código que aprovecha bien las herramientas y convenciones propias de Python, en lugar de escribirlo como si fuera C o Java traducido.

Un código pythónico:

- Usa las estructuras del lenguaje como fueron pensadas (for x in lista en vez de for i in range(len(lista))).
- Es breve, claro y directo, sin ser oscuro.
- Aprovecha las funciones y sintaxis idiomáticas del lenguaje (comprensiones, enumerate(), zip(), desempaquetado, .get() con default).
- Se lee casi como una oración en inglés.

### Ejemplo del mismo problema, resuelto de dos formas

Sumar los cuadrados de los pares del 1 al 10.

**Versión no pythónica (estilo "C traducido"):**

*Ver código en el archivo `.py` correspondiente.*

```python
suma = 0
i = 0
while i < 11:
    if i % 2 == 0:
        suma = suma + (i * i)
    i = i + 1
print(suma)
```

**Versión pythónica:**

```python
suma = sum(x**2 for x in range(11) if x % 2 == 0)
print(suma)
```

Los dos hacen exactamente lo mismo. El segundo es pythónico porque:

- Usa range() en vez de un contador manual.
- Usa una **comprensión** (generator) para filtrar y transformar en un solo paso. Comprensiones (comprehensions) lo vemos en un capítulo específico.
- Delega la suma a sum(), que ya existe.

**¿De dónde viene la palabra?**

Es una expresión nacida en la comunidad Python (no es oficial del lenguaje) para elogiar el código que "se siente natural" en Python. La contraparte es peyorativa: cuando alguien escribe C con sintaxis de Python, se dice que su código es no pythónico.

### Relación con "idiom"

**Idiom** es una construcción específica (a, b = b, a, d.get(k, 0)). **Pythónico** es el adjetivo que describe código que **usa esos idioms** y respeta las convenciones del lenguaje.

**Regla práctica:**

Si un programador Python con experiencia lee tu código y sonríe, es pythónico. Si arruga la cara y dice "esto se puede escribir mejor", no lo es.

## Cuando elegir colecciones: casos concretos

| Situación | Elegí | Por qué |
| --- | --- | --- |
| Lista de tareas pendientes con orden | Lista | Necesitás orden y modificaciones |
| Coordenadas (x, y) de un punto | Tupla | Son fijas, quizás clave de dict |
| Materias aprobadas por un alumno | Set | Sin repetidas, sin orden, búsquedas rápidas |
| Contactos: nombre ➡ teléfono | Diccionario | Cada dato tiene una etiqueta |
| Días de la semana | Tupla | Fijos, ordenados, no se modifican |
| Palabras únicas de un texto | Set | Sin repetidas |
| Configuración de una app | Diccionario | Cada opción tiene un nombre |
| Notas de un examen (con repetidas) | Lista | Necesitás repetidas y quizás orden |
| Códigos postales visitados | Set | Sin repetidos, para chequear "¿ya estuve?" |

Ante la duda: **lista**. Es la más flexible. Las otras son elecciones deliberadas cuando encajan mejor con el problema.
