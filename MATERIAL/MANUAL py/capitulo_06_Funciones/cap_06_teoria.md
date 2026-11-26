# Funciones

> Reutilizando código…

## ¿Por qué leemos este capítulo?

Hasta acá venimos escribiendo programas "en línea recta": todas las instrucciones una detrás de otra en un archivo. Funciona para ejercicios cortos, pero se rompe rápido:

- Cuando querés hacer lo mismo con datos distintos, terminás copiando y pegando código.
- Cuando encontrás un error, tenés que corregirlo en cinco lugares.
- Cuando el programa crece, se vuelve ilegible.

Las **funciones** resuelven todo eso. Una función es un bloque de código con un nombre, al que le podés pasar datos y que puede devolverte un resultado. Escribís el código una sola vez, le ponés nombre, y lo reutilizás las veces que quieras.

Ya venís usando funciones sin escribirlas:

```python
print()
input()
len()
sum()
sorted()
int()
```

En este capítulo aprenderás a construir las tuyas.

Y hay una razón extra por la que este capítulo importa mucho: **los métodos de un objeto son funciones**. Cuando lleguemos a POO, todo lo que aprendas acá se va a aplicar tal cual, con una vuelta de tuerca (el parámetro self).

Dominar funciones ahora es la mejor inversión de tiempo antes de POO.

## Definir y llamar una función

La sintaxis mínima:

```python
def saludar():
    print("¡Hola!")

saludar()      # ¡Hola!
saludar()      # ¡Hola!
saludar()      # ¡Hola!
```

Cuatro partes que conviene fijar:

- **def** — palabra reservada que le avisa a Python "acá empieza una función".
- **saludar** — el nombre. Se elige con las mismas reglas que las variables (snake_case, empieza con letra, sin espacios).
- **()** — los paréntesis. Vacíos ahora, pero acá van los parámetros.
- **:** — Los dos puntos al final son obligatorios, como en if y for.

Definir una función no la ejecuta. El código dentro del def está guardado esperando que alguien la llame. La llamada es lo que dispara la ejecución: cada saludar() corre el bloque una vez.

### Comparación con C

En C también existían las funciones, con una diferencia estructural importante:

**C**

```python
// hay que declarar tipos y usar llaves
int sumar(int a, int b) {
    return a + b;
}
```

**Python**

```python
# sin tipos, sin llaves, con dos puntos 
# e indentación
def sumar(a, b):
    return a + b
```

Python no exige declarar el tipo de los parámetros ni del retorno. Es más liviano, pero también más traicionero: nada te avisa si le pasás un string donde esperabas un número. Cuando el programa crece, esto se convierte en una fuente de bugs.

#### EJERCICIO 1

escribí una función mostrar_titulo(texto) que imprima el texto en mayúsculas rodeado de líneas de guiones. Después llamala tres veces con títulos distintos.

*Ver código en el archivo `.py` correspondiente.*

Fijate cómo la función encapsula tres líneas repetitivas. Si mañana querés cambiar los guiones por asteriscos, lo tocás en un solo lugar y afecta a las tres llamadas.

## Parámetros y argumentos

Una función se vuelve útil cuando le podés pasar datos:

```python
def saludar(nombre):
    print(f"¡Hola, {nombre}!")

saludar("Ana")      # ¡Hola, Ana!
saludar("Juan")     # ¡Hola, Juan!
```

Conviene distinguir los dos términos:

- **Parámetro:** la **variable** declarada en el def (*nombre* en el ejemplo).
- **Argumento:** el **valor concreto** que se pasa en la llamada (*"Ana", "Juan"*).

Se dice también **parámetro formal** y **argumento real**, pero en la práctica los términos se usan de forma intercambiable.

## Múltiples parámetros

```python
def presentar(nombre, edad, carrera):
    print(f"{nombre}, {edad} años, estudia {carrera}")

presentar("Ana", 22, "Ingeniería")
```

Los argumentos se asignan a los parámetros por **posición**:

- "Ana" va a nombre
- 22 a edad
- "Ingeniería" a carrera.

El orden importa.

#### EJERCICIO 2

Escribí una función calcular_area_rectangulo(base, altura) que imprima "El rectángulo de X × Y tiene área Z". Después llamala con distintos valores.

*Ver código en el archivo `.py` correspondiente.*

Con dos parámetros la función ya empieza a ser genuinamente reutilizable: cualquier combinación de base y altura funciona.

## Argumentos por nombre (keyword arguments)

También podés pasarlos por nombre, lo que hace la llamada más clara y libera al orden:

```python
presentar(nombre="Ana", edad=22, carrera="Ingeniería")
presentar(edad=22, carrera="Ingeniería", nombre="Ana")   # también funciona
```

Esto es especialmente útil cuando una función tiene muchos parámetros y no querés que el lector adivine qué es cada valor.

## Parámetros con valor por defecto

Si un parámetro tiene un valor "razonable" habitual, se lo podés dar por defecto:

```python
def saludar(nombre, saludo="Hola"):
    print(f"{saludo}, {nombre}!")

saludar("Ana")                    # Hola, Ana!
saludar("Juan", "Buen día")       # Buen día, Juan!
saludar("Pedro", saludo="Che")    # Che, Pedro!
```

### Regla clave

Los parámetros con valor por defecto van siempre al final de la lista. Esto no compila:

```python
def malo(saludo="Hola", nombre):     # SyntaxError
```

#### EJERCICIO 3

Escribí una función calcular_precio(base, iva=21, descuento=0) que devuelva el precio final aplicando primero el IVA y después el descuento (ambos en porcentaje).

*Ver código en el archivo `.py` correspondiente.*

Los defaults dejan la función flexible: quien la usa pasa solo lo que se aparta de "lo habitual".

## return: devolver un resultado

Hasta acá las funciones imprimían cosas. Pero lo más potente es que **devuelvan** un valor, para que quien las llama pueda usarlo:

```python
def sumar(a, b):
    return a + b

resultado = sumar(3, 5)
print(resultado)         # 8

total = sumar(10, 20) + sumar(30, 40)
print(total)             # 100
```

return hace dos cosas al mismo tiempo: **entrega** un valor a quien llamó, y **termina** la ejecución de la función. Cualquier código después del return no se ejecuta.

### Diferencia clave: print vs return

Esta es la confusión más frecuente al empezar:

```python
def sumar_mal(a, b):
    print(a + b)          # imprime el resultado

def sumar_bien(a, b):
    return a + b          # devuelve el resultado
```

Se ven parecidas, pero se comportan totalmente distinto:

```python
x = sumar_mal(3, 5)       # imprime 8, y x queda en None
print(x)                   # None, ups

y = sumar_bien(3, 5)      # no imprime nada, y devuelve 8
print(y)                   # 8
```

**print es un efecto lateral:** muestra algo en pantalla y ya. return produce un valor que quien llamó puede guardar en una variable, pasar a otra función, combinar con otros valores.

Un return te deja componer, un print no.

**Regla práctica:**

Una función que **calcula algo** casi siempre debería devolverlo con **return**, no imprimirlo. La decisión de qué mostrar en pantalla la deja quien la usa.

### Funciones sin return

Si una función no tiene return, o tiene un return sin valor, devuelve None (un valor especial de Python que representa "nada"):

```python
def mostrar(x):
    print(x)

resultado = mostrar(5)     # imprime 5
print(resultado)            # None
print(type(resultado))      # <class 'NoneType'>
```

Está bien tener funciones que solo hacen efecto y devuelven None (como print() mismo). Lo que no está bueno es hacerlo por error.

Acordate de poner return cuando estás calculando algo.

#### EJERCICIO 4

Escribí es_par(n) que devuelva True o False (sin imprimir nada). Después usala en un if para decidir qué imprimir.

*Ver código en el archivo `.py` correspondiente.*

Fijate cómo la función se combina con if porque **devuelve** un booleano. Si es_par hubiera hecho print("es par") en lugar de return, no habríamos podido usarla dentro del if.

### Devolver varios valores

Una función puede devolver varios valores empaquetándolos en una tupla y quien la llama los desempaqueta:

```python
def dividir_con_resto(a, b):
    return a // b, a % b    # devuelve una tupla (cociente, resto)

cociente, resto = dividir_con_resto(47, 5)
print(cociente)              # 9
print(resto)                 # 2
```

Esto es una de las razones por las que las tuplas son tan útiles en Python. En C tenías que devolver una struct o pasar punteros, acá es una línea.

#### EJERCICIO 5

Escribí una función estadisticas(numeros) que reciba una lista y devuelva la suma, el promedio, el mínimo y el máximo. Después llamala y desempaquetá los cuatro valores.

*Ver código en el archivo `.py` correspondiente.*

Fijate la simetría: el return empaqueta cuatro valores en una tupla, y la asignación los desempaqueta en cuatro variables.

## Alcance (scope) de las variables

Este tema conviene entenderlo temprano porque es fuente clásica de confusión:

```python
def modificar():
    x = 10        # x local a la función
    print(x)

x = 5             # x global
modificar()       # imprime 10
print(x)          # imprime 5 ¡no se modificó
```

La x de adentro de la función **no es** la x de afuera. Son dos variables distintas que casualmente se llaman igual. Python crea un "espacio" nuevo cada vez que se llama una función, las variables definidas ahí adentro viven solo mientras la función corre.

### Leer variables globales sí se puede

Desde adentro de una función podés **leer** variables globales:

```python
IVA = 21    # constante global

def con_iva(precio):
    return precio * (1 + IVA / 100)

print(con_iva(1000))    # 1210.0
```

Pero **modificarlas** requiere una declaración explícita (global), que es una práctica desaconsejada. Si necesitás modificar algo de afuera, es señal de que la función debería **devolverlo** con return, no cambiarlo por atrás.

**Regla práctica**

Tratá a las funciones como cajas cerradas: **entran** parámetros por adelante, **sale** un valor por atrás con **return**. Todo lo que pase adentro es asunto de la función. Este es el mismo principio de encapsulamiento que vas a ver formalizado en POO.

#### EJERCICIO 6

Predecí qué imprime este código antes de ejecutarlo, y después probalo:

*Ver código en el archivo `.py` correspondiente.*

La x de la función es local. Cuando le asignamos 999, no tocamos al numero de afuera. Los parámetros funcionan como variables locales que reciben una copia del valor.

**Ojo con listas y diccionarios:**

Con tipos mutables la cosa cambia un poco. Si le pasás una lista a una función y la modificás adentro, sí ves el cambio afuera. Vamos a esto en un momento.

## Funciones que reciben colecciones

Las funciones se llevan bien con listas, diccionarios y demás:

```python
def promedio(numeros):
    return sum(numeros) / len(numeros)

def filtrar_aprobados(notas):
    aprobados = []
    for nombre, nota in notas.items():
        if nota >= 7:
            aprobados.append(nombre)
    return aprobados

print(promedio([7, 8, 5, 9]))
print(filtrar_aprobados({"Ana": 8, "Juan": 5, "Pedro": 9}))
```

Todo lo que aprendimos en el capítulo de Colecciones se combina naturalmente con funciones. De hecho, muchas funciones útiles no son más que "un bucle envuelto con nombre".

## Cuidado con los tipos mutables

Cuando pasás una **lista** o un **diccionario** a una función y los modificás adentro, el cambio se ve afuera:

```python
def agregar_uno(lista):
    lista.append("¡nuevo!")

mis_datos = [1, 2, 3]
agregar_uno(mis_datos)
print(mis_datos)     # [1, 2, 3, '¡nuevo!'] ¡se modificó!
```

Esto es distinto de lo que pasaba con enteros y strings, que son inmutables. La razón es la misma que vimos con las etiquetas en el capítulo de datos: el parámetro y la variable de afuera son **dos etiquetas apuntando al mismo objeto**, y modificar el objeto lo cambia para las dos.

Para evitarlo, la función puede trabajar sobre una **copia**:

```python
def agregar_uno_a_copia(lista):
    nueva = lista.copy()
    nueva.append("¡nuevo!")
    return nueva

mis_datos = [1, 2, 3]
otros = agregar_uno_a_copia(mis_datos)
print(mis_datos)     # [1, 2, 3] intacto
print(otros)         # [1, 2, 3, '¡nuevo!']
```

Como principio general: si tu función **calcula un resultado nuevo**, devolvelo con return en vez de modificar los datos que recibió. Es más limpio, más predecible y fácil de testear.

#### EJERCICIO 7

Escribí duplicar(lista) que devuelva una lista nueva con cada elemento multiplicado por 2, sin modificar la original.

*Ver código en el archivo `.py` correspondiente.*

## Docstrings: documentar tus funciones

Cuando una función es no-trivial, conviene explicar qué hace. La convención en Python es usar un **docstring**: un string entre """ como primera línea del cuerpo:

```python
def calcular_imc(peso, altura):
    """Calcula el Índice de Masa Corporal.

    Recibe peso en kg y altura en metros.
    Devuelve el IMC como float.
    """
    return peso / (altura ** 2)
```

El estilo lo dicta **PEP 257** (la convención oficial de docstrings). Las reglas son:

- **Los """ de apertura van pegados al texto** (no en una línea propia con el texto abajo).
- **La primera línea es un resumen corto** (una sola oración imperativa).
- Si hay más contenido, va **una línea en blanco** después del resumen.
- **Los """ de cierre van en su propia línea** cuando el docstring tiene varias líneas.

**Regla mental**

**Corto** (una línea): todo pegado, en una sola línea física.

**Largo** (varias líneas): resumen pegado a los """ iniciales, línea en blanco, detalle, """ de cierre en línea propia.

### Beneficios reales

- Sirve de documentación para vos mismo dentro de un mes.
- help(calcular_imc) en el shell muestra el docstring.
- Herramientas como Sphinx generan documentación automática a partir de docstrings.
- VSCode los muestra al pasar el mouse sobre la función.

#### EJERCICIO 8

Agregá un docstring a la función calcular_precio que escribiste antes, y probá help(calcular_precio) en el shell.

*Ver código en el archivo `.py` correspondiente.*

En el shell, help() te muestra el docstring formateado, es tu "manual del programador" para esa función.

## Funciones como valores: el paso previo a lambda

Antes de meternos con lambda, hay un concepto que hace falta ver primero: **en Python, las funciones son valores**. Se pueden asignar a variables, pasar como parámetros y devolver desde otras funciones, igual que un número o un string.

```python
def saludar(nombre):
    return f"Hola, {nombre}"

# Asignamos la función a otra variable (sin paréntesis)
otra = saludar
print(otra("Ana"))       # Hola, Ana

# Las dos variables apuntan a la misma función
print(saludar == otra)   # True
```

Ojo con la diferencia: saludar (sin paréntesis) es **la función**, saludar("Ana") (con paréntesis) es llamarla y obtener el resultado.

### Pasar una función como argumento

Esto habilita algo muy poderoso: una función puede recibir a otra función como parámetro. Es lo que hacen sorted(), max() y min() con el parámetro key:

```python
def por_longitud(palabra):
    return len(palabra)

palabras = ["banana", "sol", "manzana", "pez"]
ordenadas = sorted(palabras, key=por_longitud)
print(ordenadas)     # ['sol', 'pez', 'banana', 'manzana']
```

Le estamos diciendo a sorted(): *"para comparar, no uses las palabras directamente, sino el resultado de aplicarles por_longitud"*. Cada palabra se convierte internamente en un número (su longitud), y sorted() ordena esos números.

Ahora imaginate que la función que querés pasar es tan trivial como por_longitud: una sola línea, no la vas a usar en ningún otro lado. Definirla con def y ponerle nombre parece exagerado. Para esos casos existe lambda.

## lambda: funciones anónimas

lambda es una forma abreviada de definir una función "de una sola expresión", sin nombre:

```python
# Estas dos formas son equivalentes:

def doble(x):
    return x * 2

doble = lambda x: x * 2
```

La sintaxis es lambda parametros: expresion. Tres cosas importantes:

- **No hay return**: el resultado de la expresión es lo que se devuelve automáticamente.
- **No hay bloques ni indentación**: todo tiene que caber en una expresión.
- **No hay nombre**: a menos que la asignes a una variable como en el ejemplo (cosa que casi nadie hace, porque para eso está def).

### El uso típico: parámetro key

En 90% de los casos, lambda aparece como argumento de otra función que espera una función. El ejemplo de recién queda así:

```python
palabras = ["banana", "sol", "manzana", "pez"]
ordenadas = sorted(palabras, key=lambda p: len(p))
print(ordenadas)     # ['sol', 'pez', 'banana', 'manzana']
```

Comparalo con la versión que usó por_longitud: son equivalentes, pero acá no tuvimos que declarar la función arriba. La lambda está exactamente donde se usa.

Otro caso clásico: ordenar tuplas o diccionarios por un campo específico.

```python
alumnos = [("Ana", 8), ("Juan", 6), ("Pedro", 9), ("Lucía", 7)]

# Ordenar por nota (segundo elemento de cada tupla)
alumnos.sort(key=lambda par: par[1])
print(alumnos)    # [('Juan', 6), ('Lucía', 7), ('Ana', 8), ('Pedro', 9)]

# El de mejor nota
mejor = max(alumnos, key=lambda par: par[1])
print(mejor)      # ('Pedro', 9)
```

par[1] extrae la nota de cada tupla. sorted/max usa ese valor para comparar.

Ya vimos esta sintaxis pasar en el capítulo de Colecciones (ejercicio 17 de las 3 palabras más frecuentes). Ahora tiene nombre y explicación.

### Cuándo NO usar lambda

lambda no es "una versión más corta y elegante de def". Es una herramienta específica. Usá def cuando:

- La función necesita más de una expresión (varios if, cálculos intermedios, side effects).
- La función merece un **nombre descriptivo** que documente qué hace.
- Vas a llamarla en más de un lugar.

Escribir sumar = lambda a, b: a + b en vez de def sumar(a, b): return a + b no gana nada y complica un poco la lectura. lambda brilla cuando es **anónima**, **corta** y **usada en el sitio**.

#### EJERCICIO 9

Tenés esta lista de productos como tuplas (nombre, precio, stock):

```python
productos = [
    ("pan", 500, 20),
    ("leche", 800, 5),
    ("queso", 1200, 3),
    ("yerba", 3500, 15)
]
```

Ordenala primero por precio, después por stock (de menor a mayor), y encontrá el producto más caro.

*Ver código en el archivo `.py` correspondiente.*

p[1] es el precio, p[2] el stock. La lambda extrae ese campo y sorted/max lo usan para comparar.
